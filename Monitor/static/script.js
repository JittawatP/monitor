document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/monitor804')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#data-table tbody');
            tableBody.innerHTML = '';  // Clear existing table data
            
            // Define the desired order of keys
            const keyOrder = [
                'date_str',
                'pqindex_input',
                'pqindex_output',
                'pqindex_acc',
                'icp_input',
                'icp_output',
                'icp_acc',
                'rde_input',
                'rde_output',
                'rde_acc',
                'rfs_input',
                'rfs_output',
                'rfs_acc',
                'v40_input',
                'v40_output',
                'v40_acc',
                'v100_input',
                'v100_output',
                'v100_acc',
                'ftir_input',
                'ftir_output',
                'ftir_acc',
                'an_input',
                'an_output',
                'an_acc',
                'bn_input',
                'bn_output',
                'bn_acc',
                'kf_input',
                'kf_output',
                'kf_acc',
                'fuel_input',
                'fuel_output',
                'fuel_acc',
                'pc_input',
                'pc_output',
                'pc_acc'
            ];

            data.forEach(row => {
                const tr = document.createElement('tr');
                keyOrder.forEach(key => {  // Loop through keys in desired order
                    const td = document.createElement('td');
                    td.textContent = row[key] || ''; // Set text content from corresponding key
                     // Apply class based on the key
                    //  if (['pqindex_input', 'pqindex_output', 'pqindex_acc', 'icp_input', 'icp_output', 'icp_acc', 'rde_input', 'rde_output', 'rde_acc', 'rfs_input', 'rfs_output', 'rfs_acc'].includes(key)) {
                    //     td.classList.add('blue-background');
                    // } else if (['v40_input', 'v40_output', 'v40_acc', 'v100_input', 'v100_output', 'v100_acc', 'ftir_input', 'ftir_output', 'ftir_acc', 'an_input', 'an_output', 'an_acc', 'bn_input', 'bn_output', 'bn_acc'].includes(key)) {
                    //     td.classList.add('yellow-background');
                    // } else if (['kf_input', 'kf_output', 'kf_acc', 'fuel_input', 'fuel_output', 'fuel_acc', 'pc_input', 'pc_output', 'pc_acc'].includes(key)) {
                    //     td.classList.add('purple-background');
                    // }
                    tr.appendChild(td);
                });
                tableBody.appendChild(tr);
            });
        })
        .catch(error => console.error('Error fetching data:', error));


    fetch('/api/dashboard')
        .then(response => response.json())
        .then(data => {
            const keyOrder = [
                { key: "pqindexacc", label: "PQ/SS", valueId: "pqss-value" },
                { key: "rdeacc", label: "RDE", valueId: "rde-value" },
                { key: "icpacc", label: "ICP", valueId: "icp-value" },
                { key: "rfsacc", label: "RFS", valueId: "rfs-value" },
                { key: "v40acc", label: "V40", valueId: "v40-value" },
                { key: "v100acc", label: "V100", valueId: "v100-value" },
                { key: "ftiracc", label: "FTIR", valueId: "ftir-value" },
                { key: "anacc", label: "AN", valueId: "an-value" },
                { key: "bnacc", label: "BN", valueId: "bn-value" },
                { key: "kfacc", label: "KF", valueId: "kf-value" },
                { key: "fuelacc", label: "FUEL", valueId: "fuel-value" },
                { key: "pcacc", label: "PC", valueId: "pc-value" },
                { key: "ferroacc", label: "FERRO Lab", valueId: "ferro-value" },
                { key: "iphacc", label: "i-pH", valueId: "iph-value" },
                { key: "graviacc", label: "Gravimetric", valueId: "gravi-value" },
                { key: "mpcacc", label: "MPC", valueId: "mpc-value" },
                { key: "ruleracc", label: "RULER", valueId: "ruler-value" },
                { key: "foamingacc", label: "Foaming", valueId: "foaming-value" },
                { key: "airrelacc", label: "Air release", valueId: "airrel-value" },
                { key: "watersepacc", label: "Water Sep", valueId: "watersep-value" },
                { key: "copperstripacc", label: "Copper Stip", valueId: "copperstrip-value" },
                { key: "rpvotacc", label: "RPVOT", valueId: "rpvot-value" },
                { key: "oilfilacc", label: "FIlterability", valueId: "oilfil-value" },
                { key: "autoigacc", label: "Auto Ignition", valueId: "autoig-value" },
                { key: "flaspointd92acc", label: "FlashPoint D92", valueId: "flaspointd92-value" },
                { key: "flaspointcloseacc", label: "FlashPoint Close", valueId: "flaspointclose-value" },
                { key: "phacc", label: "pH", valueId: "ph-value" },
                { key: "raacc", label: "Reserve A", valueId: "ra-value" }
            ];

            const gridContainer= document.querySelector('.grid-container');
            gridContainer.innerHTML = "";
            const container = document.querySelector('.container')
            const heaDer = document.createElement('div');
            heaDer.className ='dheader';
            heaDer.textContent = 'Remaining Sample';
            container.appendChild(heaDer);

            // สร้าง element สำหรับแสดงเวลาและวันที่
            const dateTimeDiv = document.createElement('div');
            dateTimeDiv.className = 'time-container';

            // ฟังก์ชันเพิ่มเวลาและวันที่ลงใน element
            function updateDateTime() {
                const currentDate = new Date();
                const options = { year: 'numeric', month: 'long', day: 'numeric'};
                const formattedDate = currentDate.toLocaleDateString('en-US', options);
                dateTimeDiv.textContent = formattedDate;
            }

            // เรียกใช้งานฟังก์ชันเพื่อให้เวลาและวันที่ปัจจุบันแสดงทันที
            updateDateTime();

            // เพิ่ม element ของเวลาและวันที่ลงใน container
            container.appendChild(dateTimeDiv);

            // วนลูปจำนวนแถวทั้งหมด แบ่งออกเป็นกลุ่มๆ ละ 7
            const numGroups = Math.ceil(keyOrder.length / 7);
            for (let group = 0; group < numGroups; group++) {
                // เริ่มต้นที่ index ของกลุ่ม
                const startIndex = group * 7;
                const endIndex = Math.min(startIndex + 7, keyOrder.length);

                // สร้างและเพิ่มแถวในกลุ่มนี้
                for (let i = startIndex; i < endIndex; i++) {
                    // สร้างและเพิ่ม label (odd row)
                    const oddDiv = document.createElement('div');
                    oddDiv.className = 'grid-item odd-row';
                    oddDiv.textContent = keyOrder[i].label;
                    gridContainer.appendChild(oddDiv);
                }

                for (let i = startIndex; i < endIndex; i++) {
                    // สร้างและเพิ่มข้อมูล (even row)
                    const evenDiv = document.createElement('div');
                    evenDiv.className = 'grid-item even-row';
                    evenDiv.textContent = data[0][keyOrder[i].key] || ''; // สมมติว่า data[0] คือข้อมูลที่ต้องการแสดง
                    gridContainer.appendChild(evenDiv);
                }
                
            }
        })
        .catch(error => console.error('Error fetching data:', error));

});
