export const globals = {
    baseUrl: 'http://127.0.0.1:5000/api',
    fetch(url, method, body) {
        const options = {
            method: method,
            credentials: 'include',
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json;charset=UTF-8",
                "x-access-token": localStorage.getItem("access_token")
            },
        }
        if(body)
            options.body = body ? JSON.stringify(body) : "{}"
        url = url.startsWith('/') ? this.baseUrl + url : url
        return fetch(url, options).catch(err => {
            throw err instanceof TypeError ? "Keine Verbindung zur API" : err
        })
    },
    fetchAuthenticated(...params) {
        return this.fetch(...params).then(response => {
            if(response.ok) {
                return response
            } else if(response.status == 401) {
                return this.fetch("/refresh", "PUT").then(res => {
                    if(res.ok) {
                        return res.json()
                    } else {
                        throw "Sie müssen sich erneut anmelden"
                    }
                }).then(data => {
                    localStorage.setItem("access_token", data.data.access_token)
                    return this.fetch(...params)
                }).then(r => {
                    if(r.ok) 
                        return r
                    else
                        throw "Etwas ist schiefgelaufen"
                })
            } else {
                throw "Etwas ist schiefgelaufen"
            }
        })
    }
}