document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('mainForm');
    const lastname = document.getElementById('lastname');
    const firstname = document.getElementById('firstname');
    const patronim = document.getElementById('patronim');
    const nationality = document.getElementById('nationality');
    const prev_school = document.getElementById('prev_school');
    const iin = document.getElementById('iin');
    const phone = document.getElementById('phone');
    const message = document.getElementById('message');

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (checkInputs()) {
            form.submit();
        }
    });

    lastname.addEventListener('input', () => {
        lastname.value = lastname.value.replace(/[^a-zA-Zа-яА-ЯёЁәңғүұқөһӘҢҒҮҰҚӨҺ-]/g, '');
        validateField(lastname, lastname.value.trim() !== '', 'Заполните фамилию ученика');
    });

    firstname.addEventListener('input', () => {
        firstname.value = firstname.value.replace(/[^a-zA-Zа-яА-ЯёЁәңғүұқөһӘҢҒҮҰҚӨҺ-]/g, '');
        validateField(firstname, firstname.value.trim() !== '', 'Заполните имя ученика');
    });

    patronim.addEventListener('input', () => {
        patronim.value = patronim.value.replace(/[^a-zA-Zа-яА-ЯёЁәңғүұқөһӘҢҒҮҰҚӨҺ-]/g, '');
    });

    nationality.addEventListener('input', () => {
        nationality.value = nationality.value.replace(/[^a-zA-Zа-яА-ЯёЁәңғүұқөһӘҢҒҮҰҚӨҺ-]/g, '');
        validateField(nationality, nationality.value.trim() !== '', 'Заполните национальность ученика');
    });

    prev_school.addEventListener('input', () => {
        validateField(prev_school, prev_school.value.trim() !== '', 'Введите прошлую школу ученика');
    });

    iin.addEventListener('input', () => {
        iin.value = iin.value.replace(/[^0-9]/g, '');
        validateIIN(iin);
    });

    phone.addEventListener('input', () => {
        validateField(phone, isPhone(phone.value.trim()), 'Неверный номер телефона');
    });

    message.addEventListener('input', () => {
        validateField(message, message.value.trim() !== '', 'Сообщение не может быть пустым');
    });

    function checkInputs() {
        let isValid = true;
        validateField(lastname, lastname.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(firstname, firstname.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(patronim, true, ''); //Allow no patronim
        validateField(nationality, nationality.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(prev_school, prev_school.value.trim() !== '', 'Это поле не может быть пустым');
        validateIIN(iin);
        validateField(phone, isPhone(phone.value.trim()), 'Неверный номер телефона');
        validateField(message, message.value.trim() !== '', 'Сообщение не может быть пустым');

        document.querySelectorAll('.form-control').forEach((control) => {
            if (control.classList.contains('error')) {
                isValid = false;
            }
        });

        return isValid;

    }

    function validateField(input, condition, errorMessage) {
        if (condition) {
            setSuccess(input);
        } else {
            setError(input, errorMessage);
        }
    }

    function setError(input, message) {
        const formControl = input.parentElement;
        const icon = formControl.querySelector('.icon');
        formControl.className = 'form-control error';
        icon.className = 'icon fas fa-times-circle';
        input.placeholder = message;
    }

    function setSuccess(input) {
        const formControl = input.parentElement;
        const icon = formControl.querySelector('.icon');
        formControl.className = 'form-control success';
        icon.className = 'icon fas fa-check-circle';
    }

    function isPhone(phone) {
        return /^\+?(\d.*){11,}$/.test(phone);
    }

    function showModal() {
        const modal = document.getElementById('successModal');
        modal.style.display = 'block';

        const closeBtn = document.querySelector('.close-button');
        closeBtn.onclick = function () {
            modal.style.display = 'none';
        };

        window.onclick = function (event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        };
    }

    var element = document.getElementById('phone');
    var maskOptions = {
        mask: '+7 (000) 000-00-00',
        lazy: false
    }
    var mask = new IMask(element, maskOptions);

    const optionMenu = document.querySelector(".select-menu"),
    selectBtn = optionMenu.querySelector(".select-btn"),
    options = optionMenu.querySelectorAll(".option"),
    sBtn_text = optionMenu.querySelector(".sBtn-text");

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
    })
});

function validateIIN(input) {
    const iinValue = input.value.trim();
    if (iinValue.length === 12) {
        setSuccess(input);
    } else {
        setError(input, 'Заполните 12 символов ИИН');
    }
}

});