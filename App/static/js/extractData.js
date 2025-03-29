function filterTable() {
    // Get all form values
    const port = document.getElementById('port').value.toLowerCase();
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDatei').value;
    const cargo = document.getElementById('cargo').value.toLowerCase();
    const vesselType = document.getElementById('vesseltype').value.toLowerCase();
    const operation = document.getElementById('operation').value.toLowerCase();
    const loadPort = document.getElementById('loadport').value.toLowerCase();
    const dischargePort = document.getElementById('dischargeport').value.toLowerCase();


    // Get all table rows (skip the header row)
    const rows = document.querySelectorAll('#sailedList tbody tr');
    
    rows.forEach(row => {
        const cells = row.cells;
        let shouldShow = true;
        
        // Port filter
        if (port && cells[0].textContent.toLowerCase().indexOf(port) === -1) {
            shouldShow = false;
        }
        
        // Date range filter
        if (startDate || endDate) {
            // Parse ETA_ATA_Date (cell index 3)
            const etaAtaDateStr = cells[3].textContent.trim();
            const etaAtaDate = parseDateFromCell(etaAtaDateStr);
            
            // Parse ETD_ATD_Date (cell index 5)
            const etdAtdDateStr = cells[5].textContent.trim();
            const etdAtdDate = parseDateFromCell(etdAtdDateStr);
            
            const startDateObj = startDate ? new Date(startDate) : null;
            const endDateObj = endDate ? new Date(endDate) : null;
            
            // Start date filter: show if ETA_ATA_Date is >= start date
            if (startDateObj && etaAtaDate < startDateObj) {
                shouldShow = false;
            }
            
            // End date filter: show if ETD_ATD_Date is <= end date
            if (endDateObj && etdAtdDate > endDateObj) {
                shouldShow = false;
            }
        }
        
        
        // Cargo filter
        if (cargo && cells[6].textContent.toLowerCase().indexOf(cargo) === -1) {
            shouldShow = false;
        }
        
        // Vessel type filter (you'll need to add this column to your table)
        if (vesselType && cells[9].textContent.toLowerCase().indexOf(vesselType) === -1) {
            shouldShow = false;
        }
        
        // Operation filter
        if (operation && cells[10].textContent.toLowerCase().indexOf(operation) === -1) {
            shouldShow = false;
        }
        
        // Load port filter
        if (loadPort && cells[11].textContent.toLowerCase().indexOf(loadPort) === -1) {
            shouldShow = false;
        }
        
        // Discharge port filter
        if (dischargePort && cells[12].textContent.toLowerCase().indexOf(dischargePort) === -1) {
            shouldShow = false;
        }
        
        // Agent filter (you'll need to add this column to your table or use another existing column)
        // if (agent && cells[X].textContent.toLowerCase().indexOf(agent) === -1) {
        //     shouldShow = false;
        // }
        
        // Show/hide row based on filters
        row.style.display = shouldShow ? '' : 'none';
    });
}

// Helper function to parse dates from your formatted cells (d/m/y)
function parseDateFromCell(dateStr) {
    const parts = dateStr.split(' ')[0].split('/'); // Split date part only
    if (parts.length === 3) {
        // Note: months are 0-indexed in JavaScript Date
        return new Date(`20${parts[2]}`, parts[1] - 1, parts[0]);
    }
    return new Date(); // Fallback if parsing fails
}

// Add event listeners to form fields to filter on change
document.getElementById('port').addEventListener('change', filterTable);
document.getElementById('startDate').addEventListener('change', filterTable);
document.getElementById('endDatei').addEventListener('change', filterTable);
document.getElementById('cargo').addEventListener('input', filterTable);
document.getElementById('vesseltype').addEventListener('change', filterTable);
document.getElementById('operation').addEventListener('change', filterTable);
document.getElementById('loadport').addEventListener('input', filterTable);
document.getElementById('dischargeport').addEventListener('input', filterTable);




// document.getElementById('exportBtn').addEventListener('click', async function() {
//     try {
//         // Get selected ports from multi-select dropdown
//         const portSelect = document.getElementById('port');
//         const selectedPorts = Array.from(portSelect.selectedOptions)
//                                 .map(option => option.value)
//                                 .filter(value => value); // Remove empty values

//         // Get all visible table rows
//         const allVisibleRows = Array.from(document.querySelectorAll('#sailedList tbody tr'))
//             .filter(row => row.style.display !== 'none');

//         // Filter rows by selected ports if any ports are selected
//         const visibleRows = selectedPorts.length > 0
//             ? allVisibleRows.filter(row => {
//                 const rowPort = row.querySelector('td:nth-child(1)').textContent.trim();
//                 return selectedPorts.includes(rowPort);
//             })
//             : allVisibleRows;

//         if (visibleRows.length === 0) {
//             alert('No data to export for the selected ports. Please check your filters.');
//             return;
//         }

//         // Create workbook
//         const workbook = new ExcelJS.Workbook();
//         workbook.creator = 'ISS Shipping';
//         workbook.created = new Date();

//         // Group rows by port
//         const portGroups = {};
//         visibleRows.forEach(row => {
//             const port = row.querySelector('td:nth-child(1)').textContent.trim();
//             if (!portGroups[port]) portGroups[port] = [];
//             portGroups[port].push(row);
//         });

//         // Get all visible header columns
//         const allHeaders = Array.from(document.querySelectorAll('#sailedList thead th'))
//             .map(th => th.textContent.trim());

//         // Create worksheet for each port
//         for (const [port, rows] of Object.entries(portGroups)) {
//             const worksheet = workbook.addWorksheet(port.substring(0, 31));

//             // Add title (merged cells A1 to last column in row 1-2)
//             const lastCol = String.fromCharCode(64 + allHeaders.length);
//             worksheet.mergeCells(`A1:${lastCol}2`);
//             const titleCell = worksheet.getCell('A1');
//             titleCell.value = `ISS SHIPPING VESSEL LINEUP FOR ${port}`;
//             titleCell.font = { bold: true, size: 16, color: { argb: 'FFFFFFFF' } };
//             titleCell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF0070C0' } };
//             titleCell.alignment = { vertical: 'middle', horizontal: 'center' };

//             // Add all headers in row 3
//             const headerRow = worksheet.addRow(allHeaders);
//             headerRow.eachCell(cell => {
//                 cell.font = { bold: true, color: { argb: 'FFFFFFFF' } };
//                 cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF4F81BD' } };
//                 cell.border = {
//                     top: { style: 'thin' }, left: { style: 'thin' },
//                     bottom: { style: 'thin' }, right: { style: 'thin' }
//                 };
//                 cell.alignment = { vertical: 'middle', horizontal: 'center' };
//             });

//             // Add data rows starting from row 4
//             rows.forEach(row => {
//                 const rowData = Array.from(row.querySelectorAll('td'))
//                     .map(cell => cell.textContent.trim());
//                 worksheet.addRow(rowData);
//             });

//             // Style data rows
//             worksheet.eachRow((row, rowNumber) => {
//                 if (rowNumber > 3) {
//                     row.eachCell(cell => {
//                         cell.border = {
//                             top: { style: 'thin' }, left: { style: 'thin' },
//                             bottom: { style: 'thin' }, right: { style: 'thin' }
//                         };
//                         cell.alignment = { vertical: 'middle', horizontal: 'center' };
//                     });
//                 }
//             });

//             // Auto-size columns
//             worksheet.columns = allHeaders.map((_, i) => ({
//                 width: Math.min(30, Math.max(10, allHeaders[i].length + 2))
//             }));
//         }

//         // Download the file
//         const buffer = await workbook.xlsx.writeBuffer();
//         const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
//         saveAs(blob, `Vessel_Lineup_${new Date().toISOString().slice(0,10)}.xlsx`);
        
//     } catch (error) {
//         console.error('Export error:', error);
//         alert('Error exporting data. See console for details.');
//     }
// });


// Function to filter table rows based on selected ports
function filterTableByPorts() {
    const portSelect = document.getElementById('port');
    const selectedPorts = Array.from(portSelect.selectedOptions)
                            .map(option => option.value)
                            .filter(port => port); // Remove empty values
    
    const allRows = document.querySelectorAll('#sailedList tbody tr');
    
    if (selectedPorts.length === 0) {
        // Show all rows if no ports selected
        allRows.forEach(row => row.style.display = '');
        return;
    }
    
    allRows.forEach(row => {
        const rowPort = row.querySelector('td:nth-child(1)').textContent.trim();
        row.style.display = selectedPorts.includes(rowPort) ? '' : 'none';
    });
}

// Initialize the port filter on page load and when selection changes
document.addEventListener('DOMContentLoaded', function() {
    const portSelect = document.getElementById('port');
    portSelect.addEventListener('change', filterTableByPorts);
    filterTableByPorts(); // Initial filter
});

// Export to Excel function
document.getElementById('exportBtn').addEventListener('click', async function() {
    try {
        // Get selected ports
        const selectedPorts = Array.from(document.getElementById('port').selectedOptions)
                                .map(option => option.value)
                                .filter(port => port);
        
        // Get all table rows (not just visible ones)
        const allRows = Array.from(document.querySelectorAll('#sailedList tbody tr'));
        
        // Filter rows by selected ports (or use all if none selected)
        const rowsToExport = selectedPorts.length > 0
            ? allRows.filter(row => {
                const rowPort = row.querySelector('td:nth-child(1)').textContent.trim();
                return selectedPorts.includes(rowPort);
            })
            : allRows;

        if (rowsToExport.length === 0) {
            alert('No data to export for the selected ports.');
            return;
        }

        // Create workbook
        const workbook = new ExcelJS.Workbook();
        workbook.creator = 'ISS Shipping';
        workbook.created = new Date();

        // Group rows by port
        const portGroups = {};
        rowsToExport.forEach(row => {
            const port = row.querySelector('td:nth-child(1)').textContent.trim();
            if (!portGroups[port]) portGroups[port] = [];
            portGroups[port].push(row);
        });

        // Get all column headers
        const allHeaders = Array.from(document.querySelectorAll('#sailedList thead th'))
                            .map(th => th.textContent.trim());

        // Create worksheets
        for (const [port, rows] of Object.entries(portGroups)) {
            const worksheet = workbook.addWorksheet(port.substring(0, 31));
            
            // Add title
            const lastCol = String.fromCharCode(64 + allHeaders.length);
            worksheet.mergeCells(`A1:${lastCol}2`);
            const titleCell = worksheet.getCell('A1');
            titleCell.value = `ISS SHIPPING VESSEL LINEUP FOR ${port}`;
            titleCell.font = { bold: true, size: 16, color: { argb: 'FFFFFFFF' } };
            titleCell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF0070C0' } };
            titleCell.alignment = { vertical: 'middle', horizontal: 'center' };

            // Add headers
            const headerRow = worksheet.addRow(allHeaders);
            headerRow.eachCell(cell => {
                cell.font = { bold: true, color: { argb: 'FFFFFFFF' } };
                cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF4F81BD' } };
                cell.border = {
                    top: { style: 'thin' }, left: { style: 'thin' },
                    bottom: { style: 'thin' }, right: { style: 'thin' }
                };
                cell.alignment = { vertical: 'middle', horizontal: 'center' };
            });

            // Add data
            rows.forEach(row => {
                const rowData = Array.from(row.querySelectorAll('td'))
                                  .map(cell => cell.textContent.trim());
                worksheet.addRow(rowData);
            });

            // Style data rows
            worksheet.eachRow((row, rowNumber) => {
                if (rowNumber > 3) {
                    row.eachCell(cell => {
                        cell.border = {
                            top: { style: 'thin' }, left: { style: 'thin' },
                            bottom: { style: 'thin' }, right: { style: 'thin' }
                        };
                        cell.alignment = { vertical: 'middle', horizontal: 'center' };
                    });
                }
            });

            // Set column widths
            worksheet.columns = allHeaders.map((_, i) => ({
                width: Math.min(30, Math.max(10, allHeaders[i].length + 2))
            }));
        }

        // Generate and download Excel file
        const buffer = await workbook.xlsx.writeBuffer();
        const blob = new Blob([buffer], { 
            type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
        });
        
        // Using FileSaver.js for reliable downloads
        saveAs(blob, `Vessel_Lineup_${new Date().toISOString().slice(0,10)}.xlsx`);
        
    } catch (error) {
        console.error('Export error:', error);
        alert('Error exporting data. Please check console for details.');
    }
});