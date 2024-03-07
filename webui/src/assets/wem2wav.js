const jsDir = "/vgmstream/"
class WorkerWrapper{
    constructor(url){
        this.symbol = 0
        this.allEvents = new Map()
        this.worker = new Worker(url)
        this.worker.addEventListener("message", event => this.messageEvent(event.data))
        this.worker.addEventListener("error", event => this.messageEvent({
            subject: "load",
            error: "Error loading {}".format(url)
        }))
        this.on("load").then(() => {
            this.loaded = true
        }, error => {
            alert(error)
        })
    }
    send(subject, ...content){
        return this.load().then(() => {
            return new Promise((resolve, reject) => {
                let symbol = ++this.symbol
                this.on(symbol).then(resolve, reject)
                return this.worker.postMessage({
                    symbol: symbol,
                    subject: subject,
                    content: content
                })
            })
        })
    }
    messageEvent(data){
        let addedType = this.allEvents.get(data.symbol || data.subject)
        if(addedType){
            addedType.forEach(callback => {
                if(data.error){
                    let error = new Error(data.error.message || data.error)
                    for(let i in data.error){
                        error[i] = data.error[i]
                    }
                    callback.reject(error)
                }else{
                    callback.resolve(data.content)
                }
            })
            this.allEvents.delete(data.subject)
        }
    }
    load(){
        if(this.loaded){
            return Promise.resolve(this.worker)
        }else if(this.loadError){
            return Promise.reject()
        }else{
            return this.on("load")
        }
    }
    on(type){
        return new Promise((resolve, reject) => {
            let addedType = this.allEvents.get(type)
            if(!addedType){
                addedType = new Set()
                this.allEvents.set(type, addedType)
            }
            addedType.add({
                resolve: resolve,
                reject: reject
            })
        })
    }
}


const cliWorker = new WorkerWrapper(jsDir + "cli-worker.js")

/**
 * 返回音频bolb的url
 * @param buffer{ArrayBuffer}
 * @return {Promise<String>}
 */
export async function convertBufferedArray(buffer){

    let f = new File([buffer], "input.wem")
    try{
        let response = await cliWorker.send("convertDir", [f], f.name)
        return response.url
    }finally{

    }
}