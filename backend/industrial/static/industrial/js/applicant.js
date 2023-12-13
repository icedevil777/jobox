document.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');
});

const button = document.getElementById('delButton');
const bsButton = new bootstrap.Button(button);

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

// let response = fetch('http://127.0.0.1:8000/api/v1/drf/', {
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json;charset=utf-8'
//     },
//     body: JSON.stringify(user)
// });


// let response = fetch('http://127.0.0.1:8000/api/v1/drf/1/', {
//     method: 'PUT',
//     headers: {
//         'Content-Type': 'application/json;charset=utf-8'
//     },
//     body: JSON.stringify(user)
// });

//
// let response = fetch('http://127.0.0.1:8000/api/v1/drf/4/', {
//     method: 'DELETE',
//     headers: {
//         'Content-Type': 'application/json;charset=utf-8'
//     },
//     body: JSON.stringify(user)
// });
//
// fetch('http://127.0.0.1:8000/api/v1/drf/6')
//     .then((data) => {
//         console.log(data.json());
//     });
//

