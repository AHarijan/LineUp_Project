var today = new Date()
const year = today.getFullYear();
const month = String(today.getMonth() +1).padStart(2,'0');
const day = String(today.getDate()).padStart(2,'0');

const currtDate = `${year}-${month}-${day}`;
document.getElementById('currentDate').value=currtDate;

const currtStatus = "Expected"
document.getElementById('CurrStatus').value=currtStatus;


function lineUpForm(){

    const Port = document.getElementById('port').value
    const Berth = document.getElementById('berth').value
    const Imo = document.getElementById('imono').value
    const VesselSlt = document.getElementById('vesselSlt').value
    const Vessel = document.getElementById('vessel').value
    const Loa = document.getElementById('loa').value
    const Beam = document.getElementById('beam').value
    const Draft = document.getElementById('draft').value
    const Cargo1 = document.getElementById('cargo1').value
    const CargoQtyF1 = document.getElementById('cargoQtyF1').value
    const cargoQtyUnits1 = document.getElementById('cargoQtyU1').value
    const vesselType = document.getElementById('vesseltype').value
    const Operation = document.getElementById('operation').value
    const CoatForn = document.getElementById('cos/for').value
    const etaDate = document.getElementById('etadate').value;
    const etaTime = document.getElementById('etatime').value;
    const etbDate = document.getElementById('etbdate').value;
    const etbTime = document.getElementById('etbtime').value;
    const etcDate = document.getElementById('etcdate').value;
    const etcTime = document.getElementById('etctime').value;
    const lastport = document.getElementById('lastport').value
    const nextport = document.getElementById('nextport').value
    const agent = document.getElementById('agent').value
    const CurrentStatus = document.getElementById('CurrStatus').value;

    const eta = etaDate + " " + etaTime;
    const etb = etbDate + " " + etbTime;
    const etc = etcDate + " " + etcTime;

    let etaDateTime = eta.trim();
    let etbDateTime = etb.trim();
    let etcDateTime = etc.trim();

    let currDate = new Date();
    let etaDateTimeObj = new Date(etaDateTime);
    let etbDateTimeObj = new Date(etbDateTime);
    let etcDateTimeObj = new Date(etcDateTime);

    if (Port ===  "") {
        alert("Port cannot be kept blank");
        return false;
    } 
    else if (Berth ===  "") {
        alert("Berth cannot be kept blank");
        return false;
    } 
    else if (Imo ===  "") {
        alert("Imo cannot be kept blank");
        return false;
    }
    else if (VesselSlt === "") {
        alert("Vessel Slt cannot be kept blank");
        return false;
    } 
    else if (Vessel === "") {
        alert("Vessel Name cannot be kept blank");
        return false;
    }
    else if (Loa === "") {
        alert("LOA cannot be kept blank");
        return false;
    }
    else if (Beam === "") {
        alert("Beam Name cannot be kept blank");
        return false;
    }
    else if (Draft === "") {
        alert("Draft cannot be kept blank");
        return false;
    }
    
    
    if (CurrentStatus === "Expected") {
        let etaNotNull = !etaDate;
        let date_currD = etaDateTimeObj < currDate;
        if (date_currD || etaNotNull) {
            alert(`When the vessel is ${CurrentStatus}:
            Arrival Date cannot be blank or a past date`);
            return false;
        }
        
    } else if (CurrentStatus === "Arrived") {
        let ataNotBlank_A = !etaDateTime.includes(" ");
        let etbNotNull = !etbDate;
        let ata_etb = etaDateTimeObj > etbDateTimeObj;
        if (ataNotBlank_A || etbNotNull || ata_etb) {
            alert(`When the vessel is ${CurrentStatus}: 
            Arrival Date & Time cannot be blank or future date. 
            Berthing Date cannot be blank or before ETA.`); 
            return false;
        }
    } else if (CurrentStatus === "At Berth") {
        let ataNotNull_B  = !etaDate;
        let etbNotNull_B = !etbDate;
        let etcNotNull = !etcDate;
        let ataNotBlank_B = !etaDateTime.includes(" ");
        let atbNotBlank_B = !etbDateTime.includes(" ");
        let ata_etb_B = etaDateTimeObj > etbDateTimeObj;
        let atb_etc = etbDateTimeObj > etcDateTimeObj;
        if (ataNotNull_B || etbNotNull_B || etcNotNull || ataNotBlank_B || atbNotBlank_B || atb_etc || ata_etb_B) {
            alert(`When the vessel is ${CurrentStatus}: 
            Arrival Date & Time cannot be blank or future date. 
            Berthing Date & Time cannot be blank or before Arrival Date.
            Depature Date cannot be blank or before Berthing Date`); 
            return false;
        }
    } else if (CurrentStatus === "Sailed") {
        let ataNotNull_B  = !etaDate;
        let etbNotNull_B = !etbDate;
        let etcNotNull = !etcDate;
        let ataNotBlank_B = !etaDateTime.includes(" ");
        let atbNotBlank_B = !etbDateTime.includes(" ");
        let atcNotBlank_B = !etcDateTime.includes(" ");
        let ata_etb_B = etaDateTimeObj > etbDateTimeObj;
        let atb_etc = etbDateTimeObj > etcDateTimeObj;
        let lastportF = lastport.trim() !== "";
        let nextportF = nextport.trim() !== "";
        let agentF = agent.trim() !== "";
        if (ataNotNull_B || etbNotNull_B || etcNotNull || ataNotBlank_B || atbNotBlank_B || atcNotBlank_B || atb_etc || ata_etb_B || !lastportF || !nextportF || !agentF) {
            alert(`When the vessel is ${CurrentStatus}: 
            Arrival Date & Time cannot be blank or future date. 
            Berthing Date & Time cannot be blank or before Arrival Date.
            Depature Date & Time cannot be blank or before Berthing Date
            Last Port cannot be blank
            Next Port cannot be blank
            Agent cannot be blank`); 
            return false;
        }
    } 
    
    if (Cargo1 ===  "") {
        alert("First Cargo cannot be kept blank");
        return false;
    } 
    else if (isNaN(CargoQtyF1) || CargoQtyF1 === "") {
        alert("Quantity for First Cargo cannot be kept blank and accepts only numbers");
        return false;
    } 
    else if (cargoQtyUnits1 ===  "") {
        alert("Unit for First Cargo cannot be kept blank");
        return false;
    } 
    else if (vesselType ===  "") {
        alert("Vessel Type cannot be kept blank");
        return false;
    } 
    else if (Operation ===  "") {
        alert("Please select the operation type");
        return false;
    } 
    else if (CoatForn ===  "") {
        alert("Please mention if vessel is coastal or foreign");
        return false;
    } 
    else if (CurrentStatus.trim() === "") {
        alert("Please fill in the form, select the current status and SUBMIT again");
        return false;
    } 
    else 
    alert("Details submitted successfully")
    return true 
    
}

function cargo2() {
    const CargoQtyF2 = document.getElementById('cargoQtyF1').value
    const CargoQtyF3 = document.getElementById('cargoQtyF1').value

    if (CargoQtyF2 === "") {
        document.getElementById('cargoqty2').value = 0;
    }

    return true; 
}


document.getElementById('exportBtn').addEventListener('click', function (event) {
    // Get the selected port
    const selectedPort = document.getElementById('port').value;

    // Check if a port is selected
    if (!selectedPort) {
        alert('Please select a port before exporting.'); // Show an alert
        return; // Stop further execution
    }

    // Proceed with the export if a port is selected
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('LineUp Data');

    // Add 3 blank rows
    worksheet.addRow([]);
    worksheet.addRow([]);
    worksheet.addRow([]);

    // Merge cells A1 to M2 and add the header
    worksheet.mergeCells('A1:K2');
    const mergedCell = worksheet.getCell('A1');
    mergedCell.value = `ISS SHIPPING VESSEL LINEUP FOR ${selectedPort}`;
    mergedCell.font = { bold: true, size: 16, color: { argb: 'FFFFFFFF' } }; // White text
    mergedCell.fill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FF0070C0' } // Blue background (hex: #0070C0)
    };
    mergedCell.alignment = { vertical: 'middle', horizontal: 'center', wrapText: true }; // Wrap text

    // Add table headers (excluding the hidden port column, Vessel Type, Charterer Agent, and the last two columns)
    const headers = [];
    const headerRows = document.querySelectorAll('#myTable thead th');
    headerRows.forEach((header, index) => {
        // Skip the hidden port column, Vessel Type, Charterer Agent, and the last two columns (Edit and Delete)
        if (
            !header.classList.contains('portColumn') &&
            !header.classList.contains('Ticon') &&
            header.innerText.trim() !== 'Vessel Type' &&
            header.innerText.trim() !== 'Charterer Agent'
        ) {
            headers.push(header.innerText.trim());
        }
    });
    worksheet.addRow(headers);

    // Style the headers
    const headerRow = worksheet.getRow(4); // Row 4 contains the headers
    headerRow.eachCell(cell => {
        cell.font = { bold: true, color: { argb: 'FFFFFFFF' } }; // White text
        cell.fill = {
            type: 'pattern',
            pattern: 'solid',
            fgColor: { argb: 'FF4F81BD' } // Dark blue background (hex: #4F81BD)
        };
        cell.border = {
            top: { style: 'thin' },
            left: { style: 'thin' },
            bottom: { style: 'thin' },
            right: { style: 'thin' },
        };
        cell.alignment = { vertical: 'middle', horizontal: 'center', wrapText: true }; // Wrap text
    });

    // Add visible table rows (excluding the hidden port column, Vessel Type, Charterer Agent, and the last two columns)
    const tableRows = document.querySelectorAll('#myTable tbody tr');
    tableRows.forEach(row => {
        // Check if the row is visible (not hidden by the filter)
        if (row.style.display !== 'none') {
            const rowData = [];
            const cells = row.querySelectorAll('td');
            cells.forEach((cell, index) => {
                // Skip the hidden port column, Vessel Type, Charterer Agent, and the last two columns (Edit and Delete)
                if (
                    !cell.classList.contains('portColumn') &&
                    !cell.classList.contains('Ticon') &&
                    !cell.classList.contains('vesselTypeColumn') && // Add this class to the Vessel Type column in your HTML
                    !cell.classList.contains('chartererAgentColumn') // Add this class to the Charterer Agent column in your HTML
                ) {
                    rowData.push(cell.innerText.trim());
                }
            });
            worksheet.addRow(rowData);
        }
    });

    // Style the table rows
    worksheet.eachRow((row, rowNumber) => {
        if (rowNumber > 4) { // Skip the header row and merged cells
            row.eachCell(cell => {
                cell.border = {
                    top: { style: 'thin' },
                    left: { style: 'thin' },
                    bottom: { style: 'thin' },
                    right: { style: 'thin' },
                };
                cell.alignment = { vertical: 'middle', horizontal: 'center' };
            });
        }
    });

    // Set fixed column widths
    worksheet.columns = [
        { width: 22 }, // Column A
        { width: 20 }, // Column B
        { width: 21 }, // Column C
        { width: 21 }, // Column D
        { width: 21 }, // Column E
        { width: 15 }, // Column F
        { width: 15 }, // Column G
        { width: 10 }, // Column H
        { width: 15 }, // Column I
        { width: 17 }, // Column J
        { width: 20 }, // Column K
    ];

    // Write the workbook to a file
    workbook.xlsx.writeBuffer().then(buffer => {
        const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `ISS_Shipping_Vessel_Lineup_${selectedPort}.xlsx`; // Dynamic file name with port name
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }).catch(error => {
        console.error('Error creating workbook:', error);
    });
});



document.addEventListener('DOMContentLoaded', function () {
    const autocompleteFields = [
        { id: 'shipper', datalistId: 'shipper-suggestions', field: 'Shipper' },
        { id: 'receiver', datalistId: 'receiver-suggestions', field: 'Receiver' },
        { id: 'principal', datalistId: 'principal-suggestions', field: 'Principal' },
        { id: 'owner', datalistId: 'owner-suggestions', field: 'Owner' },
        { id: 'lastport', datalistId: 'lastport-suggestions', field: 'LastPort' },
        { id: 'nextport', datalistId: 'nextport-suggestions', field: 'NextPort' },
        { id: 'loadPort', datalistId: 'loadPort-suggestions', field: 'LoadPort' },
        { id: 'dischargePort', datalistId: 'dischargePort-suggestions', field: 'DischargePort' },
        { id: 'cAgent', datalistId: 'cAgent-suggestions', field: 'ChartererAgent' },
        { id: 'agent', datalistId: 'agent-suggestions', field: 'OwnersAgent' },
    ];

    autocompleteFields.forEach(({ id, datalistId, field }) => {
        const inputField = document.getElementById(id);
        const datalist = document.getElementById(datalistId);

        if (inputField && datalist) {
            inputField.addEventListener('input', function () {
                const query = inputField.value.trim();
                console.log(`Input detected for field: ${field}, query: ${query}`);

                if (query.length >= 2) { // Fetch suggestions only if at least 2 characters are typed
                    fetch(`/get-autocomplete-suggestions/?query=${query}&field=${field}`)
                        .then(response => {
                            if (!response.ok) {
                                throw new Error('Network response was not ok');
                            }
                            return response.json();
                        })
                        .then(data => {
                            console.log(`Suggestions received for field: ${field}`, data);
                            datalist.innerHTML = ''; // Clear previous suggestions
                            data.forEach(value => {
                                const option = document.createElement('option');
                                option.value = value;
                                datalist.appendChild(option);
                            });
                        })
                        .catch(error => {
                            console.error('Error fetching suggestions:', error);
                        });
                } else {
                    datalist.innerHTML = ''; // Clear suggestions if query is too short
                }
            });
        } else {
            console.error(`Input field or datalist not found for field: ${field}`);
        }
    });
});