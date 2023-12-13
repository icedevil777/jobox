document.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');

    fetch(`http://127.0.0.1:8000/api/v1/drf/${id}`)
        .then((data) => {
            console.log(data.json())
        });
});


let user = {
    "name_app": "Поля при помоши JS PUT хуйут",
    "address": "PUT",
    "date_of_birth": "2022-10-03",
    "first_name": "",
    "second_name": "",
    "middle_name": "",
    "user_email": "",
    "tel": "",
    "salary": null,
    "about_app": "",
    "skills": "",
    "exp_work": "",
    "exp_company": "",
    "exp_period": "",
    "education": "",
    "education_courses": "",
    "education_skills": "",
    "education_speciality": "",
    "education_institut": "",
    "education_period": "",
    "language_skills": ""
};

const id = 9

