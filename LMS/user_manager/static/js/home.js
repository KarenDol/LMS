search = document.querySelector('.input-group input'),
table_headings = document.querySelectorAll('thead th');
table_rows = document.querySelectorAll('tbody tr'),
tableSection = document.getElementById('studentsTableBody');
var gradeSelection = "Все классы";
let counter = 1;
const optionMenu = document.querySelector(".select-menu"),
selectBtn = optionMenu.querySelector(".select-btn"),
options = optionMenu.querySelectorAll(".option"),
sBtn_text = optionMenu.querySelector(".sBtn-text");

document.addEventListener('DOMContentLoaded', function() {
    populateTable();
    if (optionMenu.classList.contains("active")) {
        optionMenu.classList.remove("active");
    }
});

// search
search.addEventListener('input', searchTable);

function searchTable() {
    table_rows.forEach((row, i) => {
        let table_data = row.textContent.toLowerCase(),
        search_data = search.value.toLowerCase();

        row.classList.toggle('hide', table_data.indexOf(search_data) < 0);
        row.style.setProperty('--delay', i / 25 + 's');
    })

    document.querySelectorAll('tbody tr:not(.hide)').forEach((visible_row, i) => {
        visible_row.style.backgroundColor = (i % 2 == 0) ? 'transparent' : '#0000000b';
    });
}

selectBtn.addEventListener("click", () => {
    if (optionMenu.classList.contains("active")) {
        optionMenu.classList.remove("active");
        let optionsContainer = optionMenu.querySelector(".options");
        optionsContainer.animate([
            { opacity: 1, visibility: "visible" },
            { opacity: 0, visibility: "hidden" }
        ], {
            duration: 150,
            fill: "forwards"
        });
    } else {
        optionMenu.classList.add("active");
        let optionsContainer = optionMenu.querySelector(".options");
        optionsContainer.animate([
            { opacity: 0, visibility: "hidden" },
            { opacity: 1, visibility: "visible" }
        ], {
            duration: 150,
            fill: "forwards"
        });
    }
});

options.forEach(option => {
    option.addEventListener("click", () => {
        let selectedOption = option.querySelector(".option-text").innerText;
        sBtn_text.innerText = selectedOption;
        let selectedClassInput = document.getElementById('selectedClassInput');
        selectedClassInput.value = selectedOption;

        let optionsContainer = optionMenu.querySelector(".options");
        optionsContainer.animate([
            { opacity: 1, visibility: "visible" },
            { opacity: 0, visibility: "hidden" }
        ], {
            duration: 100,
            fill: "forwards"
        });
        optionMenu.classList.remove("active");

        gradeSelection = selectedOption;
        populateTable();
    })
});


function populateTable() {
    tableSection.innerHTML = ''; // Clear the table first
    counter = 1; //Обнулить counter
    if (gradeSelection=='Все классы'){
        students.forEach(function(student) {
            if (student.status !== 'Лид'){
                addStudent(student);
            }
        });
    }
    else if (gradeSelection=='-') {
        students.forEach(function(student) {
            if ((student.status === 'Лид')){
                addStudent(student);
            }
        });
    }
    else{
        students.forEach(function(student) {
            if ((student.grade === Grades_dict[gradeSelection]) && (student.status === 'Акт')){
                addStudent(student);
            }
        });
    }
    table_rows = document.querySelectorAll('tbody tr');
}


function addStudent(student){
    var tr = document.createElement('tr');
    tr.innerHTML = `
        <td>${counter}</td>
        <td><a href="/student_card/${student.IIN}/">${student.Last_Name}</td>
        <td>${student.First_Name}</td>
        <td>${student.Patronim}</td>
        <td>${student.IIN}</td>
        <td>${student.phone}</td>
    `;
    tableSection.appendChild(tr);
    counter++;
}