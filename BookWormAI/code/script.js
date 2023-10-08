document.addEventListener('DOMContentLoaded', function () {
    //if(public==true){
        const fileInput = document.getElementById('fileInput');
        const titleInput = document.getElementById('titleInput');
        const authorInput = document.getElementById('authorInput');
        const timeInput = document.getElementById('timeInput');
        //const dataTable = document.getElementById('dataTable').getElementsByTagName('tbody')[0];

        // Function to create a new row
        function createNewRow() {
            const file = fileInput.value;
            const title = titleInput.value;
            const author = authorInput.value;
            const time = timeInput.value;

            // Create a new row
            const newRow = dataTable.insertRow();

            // Insert cells and set content
            const cell1 = newRow.insertCell(0);
            const cell2 = newRow.insertCell(1);
            const cell3 = newRow.insertCell(2);
            const cell4 = newRow.insertCell(3);

            cell1.innerHTML = file;
            cell2.innerHTML = title;
            cell3.innerHTML = author;
            cell4.innerHTML = time;

            // Clear input fields
            fileInput.value = '';
            titleInput.value = '';
            authorInput.value = '';
            timeInput.value = '';
        }

        // Add an event listener to each input field to trigger row creation on blur (when the field loses focus)
        fileInput.addEventListener('blur', createNewRow);
        titleInput.addEventListener('blur', createNewRow);
        authorInput.addEventListener('blur', createNewRow);
        timeInput.addEventListener('blur', createNewRow);
        console.log("loaded again")
    //}
});