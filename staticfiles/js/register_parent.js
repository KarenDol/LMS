document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('mainForm');
    const lastname = document.getElementById('lastname');
    const firstname = document.getElementById('firstname');
    const patronim = document.getElementById('patronim');
    const mvd = document.getElementById('mvd');
    const workplace = document.getElementById('workplace');
    const ID_numb = document.getElementById('ID_numb');
    const phone = document.getElementById('phone');
    const position = document.getElementById('position');

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (checkInputs()) {
            form.submit();
        }
    });

    lastname.addEventListener('input', () => {
        lastname.value = lastname.value.replace(/[^a-zA-Zа-яА-ЯёЁәңғүұқөһӘҢҒҮҰҚӨҺ-]/g, '');
        validateField(lastname, lastname.value.trim() !== '', 'Заполните фамилию родителя');
    });

    firstname.addEventListener('input', () => {
        firstname.value = firstname.value.replace(/[^a-zA-Zа-яА-ЯёЁәңғүұқөһӘҢҒҮҰҚӨҺ-]/g, '');
        validateField(firstname, firstname.value.trim() !== '', 'Заполните имя родителя');
    });

    patronim.addEventListener('input', () => {
        patronim.value = patronim.value.replace(/[^a-zA-Zа-яА-ЯёЁәңғүұқөһӘҢҒҮҰҚӨҺ-]/g, '');
    });

    mvd.addEventListener('input', () => {
        mvd.value = mvd.value.replace(/[^a-zA-Zа-яА-ЯёЁәңғүұқөһӘҢҒҮҰҚӨҺ-]/g, '');
        validateField(mvd, mvd.value.trim() !== '', 'Введите орган выдавший удостоверение');
    });

    workplace.addEventListener('input', () => {
        validateField(workplace, workplace.value.trim() !== '', 'Заполните место работы');
    });

    ID_numb.addEventListener('input', () => {
        ID_numb.value = ID_numb.value.replace(/[^0-9]/g, '');
        validateID(ID_numb);
    });

    let phoneMask;

    function applyPhoneMask() {
        phoneMask = IMask(phone, {
            mask: '+{7} (000) 000 0000',
            lazy: false, // show placeholder (defaults to true)
            placeholder: '7 (___) ___-____',
        });
    }

    applyPhoneMask();

    phone.addEventListener('input', () => {
        phone.value = phone.value.replace(/[^0-9]/g, '');
        validateField(phone, isPhone(phone.value.trim()), 'Неверный номер телефона');
    });

    position.addEventListener('input', () => {
        position.value = position.value.replace(/[^a-zA-Zа-яА-ЯёЁәңғүұқөһӘҢҒҮҰҚӨҺ-]/g, '');
        validateField(position, position.value.trim() !== '', 'Введите должность');
    });

    function checkInputs() {
        let isValid = true;
        validateField(lastname, lastname.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(firstname, firstname.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(address, address.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(mvd, mvd.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(workplace, workplace.value.trim() !== '', 'Это поле не может быть пустым');
        validateID(ID_numb);
        validateField(phone, isPhone(phone.value.trim()), 'Неверный номер телефона');
        validateField(patronim, true, ''); //Allow no patronim
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

function validateID(input) {
    const ID_value = input.value.trim();
    if (ID_value.length === 9) {
        setSuccess(input);
    } else {
        setError(input, 'Заполните 9 символов номера удостоверения');
    }
}

});

