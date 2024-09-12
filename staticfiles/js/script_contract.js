document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('mainForm');
    const name = document.getElementById('name');
    const fullcost = document.getElementById('fullcost');
    const discount = document.getElementById('discount');
    const monthly = document.getElementById('monthly');
    const joinfee = document.getElementById('joinfee');

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (checkInputs()) {
            form.submit();
        }
    });

    fullcost.addEventListener('input', () => {
        validateField(fullcost, fullcost.value.trim() !== '', 'Заполните сумму');
    });

    discount.addEventListener('input', () => {
        validateField(discount, discount.value.trim() !== '', 'Заполните сумму скидки');
    });

    monthly.addEventListener('input', () => {
        validateField(monthly, monthly.value.trim() !== '', 'Заполните сумму скидки');
    });

    joinfee.addEventListener('input', () => {
        validateField(joinfee, joinfee.value.trim() !== '', 'Заполните вступительный взнос');
    });

    function checkInputs() {
        let isValid = true;
        validateField(fullcost, fullcost.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(discount, discount.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(monthly, monthly.value.trim() !== '', 'Это поле не может быть пустым');
        validateField(joinfee, joinfee.value.trim() !== '', 'Это поле не может быть пустым');

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



});

