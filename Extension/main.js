function getapidata()
{
if (window.location.href.match(/^https:\/\/www\.amazon\.in\/.*\/dp\/.*$/) || window.location.href.match(/^https:\/\/www\.amazon\.in\/dp\/.*$/) ) 
{
    let product = document.evaluate('//*[@id="productTitle"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.innerText;
    let modifiedPromise = new Promise((resolve) => {
        resolve(product.replace(/\/|\\/g, " "));
    });
    modifiedPromise.then((product) => {
        fetch(`https://44hfx1.deta.dev/flipkart/${product}`).then(response => response.json()).then(data => {
        chrome.runtime.sendMessage({data: data,type:"data"});
        });
    });
    
} 
else if(window.location.href.match(/^https:\/\/www\.flipkart\.com\/.*\/p\/.*$/)) 
{
    let product = document.getElementsByClassName("B_NuCI")[0].innerText;
    let modifiedPromise = new Promise((resolve) => {
        resolve(product.replace(/\/|\\/g, " "));
    });
    modifiedPromise.then((product) => {
    fetch(`https://44hfx1.deta.dev/amazon/${product}`).then(response => response.json()).then(data => {
        chrome.runtime.sendMessage({data: data,type:"data"});
    });
    });
} 
else if(window.location.href.match(/^https:\/\/www\.amazon\.in\/s\?/)) 
{
    let searchQuery = new URL(window.location.href).searchParams.get("k");
    let product = searchQuery.split("+").join(" ");
    let modifiedPromise = new Promise((resolve) => {
        resolve(product.replace(/\/|\\/g, " "));
    });
    modifiedPromise.then((product) => {
    fetch(`https://44hfx1.deta.dev/flipkart/${product}`).then(response => response.json()).then(data => {
        chrome.runtime.sendMessage({data: data,type:"data"});
    });
    });
} 
else if(window.location.href.match(/^https:\/\/www\.flipkart\.com\/search\?/)) 
{
    let product = new URL(window.location.href).searchParams.get("q");
    let modifiedPromise = new Promise((resolve) => {
        resolve(product.replace(/\/|\\/g, " "));
    });
    modifiedPromise.then((product) => {
    fetch(`https://44hfx1.deta.dev/amazon/${product}`).then(response => response.json()).then(data => {
        chrome.runtime.sendMessage({data: data,type:"data"});
    });
    });
}
}

getapidata();
