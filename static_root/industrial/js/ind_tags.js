function delete_tags() {
    tag_arr.length = 0;
    console.log("delete tag_arr", tag_arr)

    var main = document.getElementById("main");
    if (main) {
        main.parentNode.removeChild(main);
        // main.remove();
        const my_div = document.getElementById("org_div");
        const main_div = document.createElement('div');
        main_div.setAttribute('id', "main");
        my_div.appendChild(main_div);

        var host = window.location.protocol + "//" + window.location.host;
        console.log('host', host);
        fetch(`${host}/industrial/delete_tags/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(job_id)
        });
    }
}

function clear1(teg) {

    for (let i = 0; i < tag_arr.length; i++) {
        if (teg === tag_arr[i]) {
            // delete tag_arr[i];
            tag_arr.splice(i, 1)
            console.log('tag_arr', tag_arr)

        }
    }

}

function check_array(val) {

    for (let i = 0; i < tag_arr.length; i++) {
        if (tag_arr[i] === val) {
            console.log('есть в списке');
            is = true;
        }
    }
    if (is === false) {
        tag_arr.push(val);
        return true;
    } else {
        is = false;
        return false;
    }
}

function add_new_tag() {

    const val = document.getElementById("job-ind-tag").value;
    const my_div = document.getElementById("main");

    const dv = document.createElement('div');
    dv.classList.add('form-check', 'form-check-inline');
    dv.setAttribute('id', "my1_div");


    const inp = document.createElement('input');
    inp.classList.add('form-check-input');
    inp.setAttribute('style', 'font-size: inherit;');
    inp.setAttribute('type', 'checkbox');
    inp.setAttribute('checked', 'checked');
    inp.setAttribute('id', `${val}`);


    const lab = document.createElement('label');
    lab.classList.add('form-check-label');
    lab.setAttribute('for', `${val}`);
    lab.textContent = `${val}`

    if (val.length > 0 && check_array(val)) {
        my_div.appendChild(dv);
        dv.appendChild(inp);
        dv.appendChild(lab);

        const data = document.createElement('input');
        data.classList.add('data-input');
        data.setAttribute('type', 'hidden');
        data.setAttribute('name', 'new_ind_tag_data');
        data.setAttribute('value', `${tag_arr}`);
        dv.appendChild(data);
        console.log('tag_arr', tag_arr)
    }
}
