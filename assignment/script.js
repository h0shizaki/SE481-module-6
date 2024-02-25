const searchBtn = document.querySelector("#searchBtn")
const queryInput = document.querySelector("#queryInput")
const tableTab = document.querySelector("#tableTab")
const API_URL = "http://localhost:5000/manual_index"
const search = async(e) => { 
    console.log("Test")
    let query = queryInput.value
    const data = await fetch(API_URL+"?query="+query)
    res = (await data.json())

    console.log(res);
    res = res.results

    tableTab.innerHTML = "";
    // Create table header
    const tableHeader = document.createElement("tr");
    const headers = ["Title", "URL", "Text", "Score"];
    headers.forEach(header => {
        const th = document.createElement("th");
        th.textContent = header;
        tableHeader.appendChild(th);
    });
    tableTab.appendChild(tableHeader);
    res.forEach(result => {
        const row = document.createElement("tr");
        const keys = ["title", "text", "score", "pagerank"];
        keys.forEach(key => {
            const cell = document.createElement("td");
            if (key === "text") {
                const text = result[key];
                const index = text.toLowerCase().indexOf(query.toLowerCase());
                let startIndex = Math.max(0, index - 50);
                let endIndex = Math.min(text.length, index + query.length + 50);
                let surroundingText = text.substring(startIndex, endIndex);
                if (startIndex > 0) {
                    surroundingText = "... " + surroundingText;
                }
                if (endIndex < text.length) {
                    surroundingText += " ...";
                }
                const highlightedText = surroundingText.replace(new RegExp(query, "gi"), match => `<b>${match}</b>`);
                cell.innerHTML = highlightedText;
            } else {
                cell.textContent = result[key];
            }
            row.appendChild(cell);
        });
        tableTab.appendChild(row);
    });

}