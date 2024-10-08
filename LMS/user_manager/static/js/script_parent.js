document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('mainForm');
    const lastname = document.getElementById('lastname');
    const firstname = document.getElementById('firstname');
    const patronim = document.getElementById('patronim');
    const mvd = document.getElementById('mvd');
    const workplace = document.getElementById('workplace');
    const iin = document.getElementById('iin');
    const phone = document.getElementById('phone');
    const position = document.getElementById('position');

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (checkInputs()) {
            form.submit();
        }
    });

    lastname.addEventListener('input', () => {
        validateField(lastname, lastname.value.trim() !== '', 'Заполните фамилию родителя');
    });

    firstname.addEventListener('input', () => {
        validateField(firstname, firstname.value.trim() !== '', 'Заполните имя родителя');
    });

    mvd.addEventListener('input', () => {
        validateField(mvd, mvd.value.trim() !== '', 'Заполните номер удостоверения');
    });

    workplace.addEventListener('input', () => {
        validateField(workplace, workplace.value.trim() !== '', 'Заполните место работы');
    });

    iin.addEventListener('input', () => {
        validateIIN(iin);
    });

    phone.addEventListener('input', () => {
        validateField(phone, isPhone(phone.value.trim()), 'Неверный номер телефона');
    });

    patronim.addEventListener('input', () => {
        validateField(patronim, patronim.value.trim() !== '', 'Заполните отчество родителя');
    });

    position.addEventListener('input', () => {
        validateField(position, position.value.trim() !== '', 'Введите должность');
    });

    function checkInputs() {
        let isValid = true;
        validateField(lastname, lastname.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(firstname, firstname.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(address, address.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(mvd, mvd.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(workplace, workplace.value.trim() !== '', 'Это поле не может быть пустым');
        validateIIN(iin);
        validateField(phone, isPhone(phone.value.trim()), 'Неверный номер телефона');
        validateField(patronim, patronim.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(position, position.value.trim() !== '', 'Это поле не может быть пустым');

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

function validateIIN(input) {
    const iinValue = input.value.trim();
    if (iinValue.length === 7) {
        setSuccess(input);
    } else {
        setError(input, 'Заполните 7 символов номера удостоверения');
    }
}

});

