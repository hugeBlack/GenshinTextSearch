import os
from struct import Struct, unpack, pack
from io import BytesIO
from re import compile as re_compile
UNICODE_STRING = 2
ASCII_STRING = 1
FILL_PATTERN = b'\xFF'


# 内置字节转数字封装函数
def byte2num(byt):
	return int.from_bytes(byt, byteorder='little')


# TODO 日志模块
class Log:
	def __init__(self, fobj):
		pass


class PackageFormatError(Exception):
	pass


def get_string(fobj, location, string_mode):
	fobj.seek(location, 0)
	name = []
	while True:
		tmpchar = byte2num(fobj.read(string_mode))
		if tmpchar:
			name.append(chr(tmpchar))
		else:
			break
	return ''.join(name)


# 读取字典，文件对象一定要定位到字典开头
def _load_files(table_buffer, files_map, lang_map, file_index, hashmode=1):
	# 初始化信息解包
	filenum = byte2num(table_buffer.read(4))
	if filenum:
		if hashmode == 2:
			tmpstru = r'<Q4I'
			info_length = 24
		elif hashmode == 1:
			tmpstru = r'<5I'
			info_length = 20
		else:
			raise Exception('不支持8字节以上hash')
		info_struct = Struct(tmpstru)
		del tmpstru
		# 获取文件数量
		for i in range(filenum):
			hashsum, multi, file_size, offset, lang = info_struct.unpack(table_buffer.read(info_length))
			# 添加包id和音频id
			lang = lang_map[lang]
			if lang not in files_map:
				stream_map = {}
				files_map[lang] = stream_map
			else:
				stream_map = files_map[lang]
			if hashsum not in stream_map:
				stream_map[hashsum] = [(file_index, file_size, offset * multi)]
			else:
				stream_map[hashsum].append((file_index, file_size, offset * multi))


class Package:
	# 初始化查询字典
	def __init__(self, string_mode=UNICODE_STRING, log=None):
		self.LANGUAGE_DEF = {
			'CHINESE': 2,
			'ENGLISH(US)': 1,
			'JAPANESE': 3,
			'KOREAN': 4,
			"SFX": 0
		}
		self._string_mode = string_mode
		self.streamfiles_map = {}
		self.sbfiles_map = {}
		self.sbtitles_map = {}
		self.map = (self.sbtitles_map, self.sbfiles_map, self.streamfiles_map)
		self.file_list = []
		self._log = log

	# 添加包
	def addfile(self, fobj):
		# 判断文件头
		if fobj.read(4) != b'AKPK':
			assert '格式不正确'
		# 解包偏移参数
		header_size, pck_version, languages_size, sbtitles_size, sbfiles_size, streamfiles_size = unpack('<6I', fobj.read(24))
		if pck_version != 1:
			if self._log:
				self._log.logging(r'包版本：' + str(pck_version))
		lang_def_trans_map = self._load_language_def(BytesIO(fobj.read(languages_size)))

		file_index = len(self.file_list)
		self.file_list.append(fobj)
		self._load_bank_title(BytesIO(fobj.read(sbtitles_size)), lang_def_trans_map, file_index)
		self._load_bank_file(BytesIO(fobj.read(sbfiles_size)), lang_def_trans_map, file_index)
		self._load_stream_file(BytesIO(fobj.read(streamfiles_size)), lang_def_trans_map, file_index)

	# 根据hash获取文件数据
	def get_file_data_by_hash(self, hash_num, langid=0, mode=0, get_latest=True):
		hash_info = self.map[mode]
		hashmap = hash_info[langid]
		if hash_num not in hashmap:
			raise FileNotFoundError('找不到对应文件')
		if get_latest:
			hash_data = hashmap[hash_num][-1:]
		else:
			hash_data = hashmap[hash_num]
		result = []
		for j in hash_data:
			file_id, file_size, file_offset = j
			fobj = self.file_list[file_id]
			fobj.seek(file_offset, 0)
			try:
				fname = fobj.name
			except AttributeError:
				fname = 'Unknown'
			result.append((fobj.read(file_size), fname))
		return result

	def check_file_by_hash(self, hash_num, langid=0, mode=0):
		hash_info = self.map[mode]
		hashmap = hash_info[langid]
		return hash_num in hashmap

	def del_hash_files(self, hash_num, mode):
		hash_map = self.map[mode]
		for i in hash_map:
			maps = hash_map[i]
			if hash_num in maps:
				del maps[hash_num]

	def add_wem(self, mode, lang_id, hash_num, wem_file_obj):
		hash_map = self.map[mode]
		ind = len(self.file_list)
		self.file_list.append(wem_file_obj)
		wem_file_obj.seek(0, 2)
		file_size = wem_file_obj.tell()
		wem_file_obj.seek(0, 0)
		data = (ind, file_size, 0)
		if lang_id in hash_map:
			if hash_num not in hash_map[lang_id]:
				hash_map[lang_id][hash_num] = []
			hash_map[lang_id][hash_num].append(data)
		else:
			hash_map[lang_id] = {hash_num: [data]}

	def _load_language_def(self, bytestream):
		mapnum = byte2num(bytestream.read(4))
		lang_map = {}
		unpacker = Struct('<2I')
		for i in range(mapnum):
			offset, lang_id = unpacker.unpack(bytestream.read(8))
			lang_map[lang_id] = offset
		for i in lang_map:
			lang = get_string(bytestream, lang_map[i], self._string_mode).upper()
			if lang not in self.LANGUAGE_DEF:
				self.LANGUAGE_DEF[lang] = len(self.LANGUAGE_DEF)
			lang_map[i] = self.LANGUAGE_DEF[lang]
		return lang_map

	def _load_bank_title(self, table_buffer, lang_map, file_index):
		_load_files(table_buffer, self.sbtitles_map, lang_map, file_index, hashmode=1)

	def _load_bank_file(self, table_buffer, lang_map, file_index):
		_load_files(table_buffer, self.sbfiles_map, lang_map, file_index, hashmode=1)

	def _load_stream_file(self, table_buffer, lang_map, file_index):
		_load_files(table_buffer, self.streamfiles_map, lang_map, file_index, hashmode=2)

	def _check_for_language(self, language):
		if type(language).__name__ == 'str':
			if language not in self.LANGUAGE_DEF:
				raise Exception('找不到对应语言')
			language = self.LANGUAGE_DEF[language]
		return language

	def __del__(self):
		for i in self.file_list:
			i.close()


# class AsyncNetworkPackage(Package):
# 	from aiohttp import ClientSession
#
# 	def __init__(self, session: ClientSession = None):
# 		if not session:
# 			self.session = self.ClientSession(skip_auto_headers=('User-Agent',))
# 		else:
# 			self.session = session
# 		super().__init__()
#
# 	async def addfile(self, url):
# 		"""异步读取网络pck文件"""
# 		# 判断文件头
# 		fobj = await self.session.get(url)
# 		if await fobj.content.read(4) != b'AKPK':
# 			fobj.close()
# 			raise PackageFormatError
# 		# 解包偏移参数
# 		header_size, pck_version, languages_size, sbtitles_size, sbfiles_size, streamfiles_size\
# 			= unpack('<6I', await fobj.content.read(24))
# 		if pck_version != 1:
# 			if self._log:
# 				self._log.logging(r'包版本：' + str(pck_version))
# 		lang_def_trans_map = self._load_language_def(BytesIO(await fobj.content.read(languages_size)))
#
# 		file_index = len(self.file_list)
# 		self.file_list.append(url)
# 		bank_title_data = BytesIO(await fobj.content.read(sbtitles_size))
# 		bank_file_data = BytesIO(await fobj.content.read(sbfiles_size))
# 		stream_file_data = BytesIO(await fobj.content.read(streamfiles_size))
# 		fobj.close()
# 		self._load_bank_title(bank_title_data, lang_def_trans_map, file_index)
# 		self._load_bank_file(bank_file_data, lang_def_trans_map, file_index)
# 		self._load_stream_file(stream_file_data, lang_def_trans_map, file_index)
#
# 	async def add_wem(self, mode, lang_id, hash_num, wem_file_obj):
# 		"""异步读取本地文件（应该没有人直接下载wem文件吧）"""
# 		hash_map = self.map[mode]
# 		ind = len(self.file_list)
# 		self.file_list.append(wem_file_obj)
# 		await wem_file_obj.seek(0, 2)
# 		file_size = await wem_file_obj.tell()
# 		await wem_file_obj.seek(0, 0)
# 		data = (ind, file_size, 0)
# 		if lang_id in hash_map:
# 			if hash_num not in hash_map[lang_id]:
# 				hash_map[lang_id][hash_num] = []
# 			hash_map[lang_id][hash_num].append(data)
# 		else:
# 			hash_map[lang_id] = {hash_num: [data]}
#
# 	async def get_file_data_by_hash(self, hash_num, langid=0, mode=0, get_latest=True, need_name=False):
# 		hash_info = self.map[mode]
# 		hashmap = hash_info[langid]
# 		if hash_num not in hashmap:
# 			raise FileNotFoundError('找不到对应文件')
# 		if get_latest:
# 			hash_data = hashmap[hash_num][-1:]
# 		else:
# 			hash_data = hashmap[hash_num]
# 		result = []
# 		for j in hash_data:
# 			file_id, file_size, file_offset = j
# 			url = self.file_list[file_id]
# 			async with self.session.request('GET', url, headers={'range': f'bytes={file_offset}-{file_offset + file_size - 1}'}) as fobj:
# 				if need_name:
# 					result.append((await fobj.read(), os.path.basename(url).split('?')[0]))
# 				else:
# 					result.append(await fobj.read())
# 		return result
#
# 	def __del__(self):
# 		self.session.close()


def fnv_hash_64(data: str):
	hash_num = 14695981039346656037
	data = data.lower().encode()
	# print(data)
	for i in data:
		hash_num = ((hash_num * 1099511628211) & 0xffffffffffffffff) ^ i
	return hash_num


def fnv_hash_32(data: str):
	hash_num = 2166136261
	data = data.lower().encode()
	for i in data:
		hash_num = ((hash_num * 16777619) & 0xffffffff) ^ i
	return hash_num


def compare_new_files(csfpath, zsfpath, outputpath, re_code):
	def loadpackage(path):
		os.chdir(path)
		a = Package()
		for i in os.listdir(r'./'):
			if os.path.isfile(i):
				if searchfunc.fullmatch(i):
					a.addfile(open(i, 'rb'))
		return a

	searchfunc = re_compile(re_code + r".pck")
	csf_package = loadpackage(csfpath)
	zsf_package = loadpackage(zsfpath)
	a = set(csf_package.streamfiles_map[0][0])
	b = set(zsf_package.streamfiles_map[0][0])
	c = a-b
	print('加载完成')
	for i in c:
		os.chdir(outputpath)
		with open(str(i) + '.wem', 'wb') as f:
			data = csf_package.get_file_data_by_hash(i, 0, 2)[-1][0]
			f.write(data)


def build_pck_file(class_obj, fobj, language_def):
	# 处理字符串map
	def str_encoder(name: str):
		encoded_bytes = BytesIO()
		lens = class_obj._string_mode
		for i in name:
			encoded_bytes.write(num2bytes(ord(i), lens))
		encoded_bytes.write(num2bytes(0, lens))
		return encoded_bytes.getvalue()

	def num2bytes(num, lens=4):
		return num.to_bytes(lens, byteorder='little')

	def build_language_map(lang_id):
		lang_str = []  # 存储预处理的String信息
		lang_id.sort()  # 预排序LanguageId
		langdel = {language_def[i]: i.lower() for i in language_def}  # 预处理LanguageDef
		for i in lang_id:
			lang_str.append(str_encoder(langdel[i]))  # 预处理String为bytes
		del langdel
		lens = len(lang_id)
		lang_str_offset = 8 * lens + 4
		fbuf = BytesIO()
		fbuf.write(num2bytes(lens))
		lang_str_count = 0
		for i in lang_id:
			fbuf.write(num2bytes(lang_str_offset))  # 写入字符串偏移量
			fbuf.write(num2bytes(i))  # 写入LanguageId
			lang_str_offset += len(lang_str[lang_str_count])  # 计算下一个字符串偏移量
			lang_str_count += 1
		for i in lang_str:
			fbuf.write(i)  # 写入字符串信息
		return fbuf.getvalue()

	# 预先计算大小，排序hash，除此之外返回使用语言id和文件位置大小信息
	def pre_calculate_files_info(mode, if_output_file_size):
		size = 1
		hash_data = {}
		base_count = (5, 5, 6)[mode]
		files_size = 0
		smap = class_obj.map[mode]
		lang_id = list(smap.keys())
		for single_lang in lang_id:
			lang_map = smap[single_lang]
			lens = len(lang_map)
			if lens:
				size += lens * base_count
			for i in lang_map:
				info = lang_map[i][-1]
				if if_output_file_size:
					files_size += info[1]
				try:
					hash_data[i][single_lang] = info
				except KeyError:
					hash_data[i] = {single_lang: info}

		return size * 4, lang_id, sorted(hash_data.items(), key=lambda d: d[0]), files_size

	def build_file_map(mode, map_data, init_offset):
		if mode:
			unpack_code = r'<5I'
		else:
			unpack_code = r'<Q4I'
		packer = Struct(unpack_code)
		file_list = []
		fobj.write(num2bytes(len(map_data)))
		for hash_info in map_data:
			hash_num, value = hash_info
			value = sorted(value.items(), key=lambda d: d[0])
			for i in value:
				offset_multiplicand = (init_offset >> 32) + 1
				offset_multiplier = ceil(init_offset/offset_multiplicand)
				fill_bytes = init_offset % offset_multiplicand
				if fill_bytes:
					print(fill_bytes)
				lang_id, i = i
				package_id, file_size, origin_offset = i
				file_list.append((package_id, file_size, origin_offset, fill_bytes))
				fobj.write(packer.pack(hash_num, offset_multiplicand, file_size, offset_multiplier, lang_id))
				init_offset += (fill_bytes + file_size)

		return file_list

	def write_audio_data(file_list):
		for package_id, file_size, origin_offset, fill_bytes in file_list:
			file = class_obj.file_list[package_id]
			file.seek(origin_offset, 0)
			fobj.write(file.read(file_size))
			if fill_bytes:
				fobj.write(FILL_PATTERN * fill_bytes)

	from math import ceil
	# 构建文件头
	fobj.write(b'AKPK')  # 文件magic

	# 预处理计算数据
	bt_size, bt_langid, bt_hash, bt_file_size = pre_calculate_files_info(0, True)
	bf_size, bf_langid, bf_hash, bf_file_size = pre_calculate_files_info(1, True)
	sf_size, sf_langid, sf_hash, _ = pre_calculate_files_info(2, True)

	# 构造LanguageMap
	langid = list(set(bt_langid + bf_langid + sf_langid))
	del bt_langid, bf_langid, sf_langid
	language_map = build_language_map(langid)
	language_map_size = len(language_map)

	# 计算偏移量
	header_size = language_map_size + bt_size + bf_size + sf_size + 20
	fobj.write(pack('<6I', header_size, 1, language_map_size, bt_size, bf_size, sf_size))
	del bt_size, bf_size, sf_size

	# 写入LanguageMap
	fobj.write(language_map)
	header_size += 8

	# 构造FileLUT并写入
	bt_file_write_info = build_file_map(1, bt_hash, header_size)
	del bt_hash
	header_size += bt_file_size

	bf_file_write_info = build_file_map(1, bf_hash, header_size)
	del bf_hash
	header_size += bf_file_size

	sf_file_write_info = build_file_map(0, sf_hash, header_size)
	del sf_hash

	# 写入音频文件数据
	write_audio_data(bt_file_write_info)
	write_audio_data(bf_file_write_info)
	write_audio_data(sf_file_write_info)

