function showTable() {
    hideAllSections();
    document.getElementById("tableSection").style.display = "block";
}

function showImages(sectionId) {
    hideAllSections();
    document.getElementById(sectionId).style.display = "block";
}

function viewFullscreen(imageSrc) {
    var fullscreenImage = document.createElement("img");
    fullscreenImage.src = imageSrc;
    fullscreenImage.alt = "Fullscreen Image";
    fullscreenImage.className = "image-fullscreen";
    
    var fullscreenContainer = document.createElement("div");
    fullscreenContainer.appendChild(fullscreenImage);
    
    fullscreenContainer.style.position = "fixed";
    fullscreenContainer.style.top = "0";
    fullscreenContainer.style.left = "0";
    fullscreenContainer.style.width = "100%";
    fullscreenContainer.style.height = "100%";
    fullscreenContainer.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
    fullscreenContainer.style.display = "flex";
    fullscreenContainer.style.justifyContent = "center";
    fullscreenContainer.style.alignItems = "center";
    
    fullscreenContainer.onclick = function () {
        fullscreenContainer.remove();
    };
    
    document.body.appendChild(fullscreenContainer);
}

function hideAllSections() {
    var sections = document.getElementsByTagName("section");
    for (var i = 0; i < sections.length; i++) {
        sections[i].style.display = "none";
    }
}

function showTable() {
    hideAllSections();
    document.getElementById("tableSection").style.display = "block";
    populateTableFromCSV("data.csv");
}

function populateTableFromCSV(csvFile) {
    var table = document.getElementById("data-table");
    table.innerHTML = ""; // Clear existing table content

    // Fetch the CSV file
    fetch(csvFile)
        .then(response => response.text())
        .then(data => {
            // Parse CSV data
            var rows = data.split('\n');
            for (var i = 0; i < rows.length; i++) {
                var cells = rows[i].split(',');
                var row = table.insertRow();
                for (var j = 0; j < cells.length; j++) {
                    var cell = row.insertCell();
                    // Check if it's the last row and last column
                    if (i === 0 && j === cells.length - 1) {
                        // Display the title instead of a link in the first row
                        cell.textContent = cells[j];
                    } else if (j === cells.length - 1 && cells[j].trim() !== "") {
                        // Check if the cell contains a filename
                        var link = document.createElement("a");
                        link.href = "output_analysis/" + cells[j].trim();
                        link.textContent = "📄 Download File";
                        link.download = cells[j].trim();//"resume_" + cells[0].toLowerCase() + "." + cells[j].split('.').pop();
                        cell.appendChild(link);
                    } else {
                        cell.textContent = cells[j];
                    }
                }
            }
        })
        .catch(error => console.error('Error fetching CSV:', error));
}

