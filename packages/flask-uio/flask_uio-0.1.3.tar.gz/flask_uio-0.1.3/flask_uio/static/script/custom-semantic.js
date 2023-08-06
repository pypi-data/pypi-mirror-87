function load_date_field(id, format) {
    $("#" + id).calendar(
        {
            type: 'date',
            formatInput: false,
            formatter: {
                date: function (date, settings) {
                    if (!date) { return ''; }
                    return $.format.date(date, format);
                },
            }
        }
    );
}

function load_datetime_field(id, format) {
    $("#" + id).calendar(
        {
            type: 'datetime',
            formatInput: false,
            formatter: {
                datetime: function (date, settings) {
                    if (!date) { return ''; }
                    return $.format.date(date, format);
                },
            }
        }
    );
}

function load_checkbox_field(id) {
    $("#" + id).checkbox();
}

function load_dropdown_field(id) {
    $("#" + id).dropdown({
        ignoreDiacritics: true,
        fullTextSearch: 'exact',
    });
}

function load_dropdown(id, option={}) {
    if (jQuery.isEmptyObject(option)){
        $("#" + id).dropdown();    
    }else{
        $("#" + id).dropdown(option);
    }
}

function load_relationship_dropdown_field(id, dependents = []) {    
    $("#" + id).dropdown({
        ignoreDiacritics: true,
        fullTextSearch: 'exact',
    });

    const parent = document.getElementById(id);
    $("#" + id).change(function(){
        for(let dependent of dependents){
            let selected_value = 0;
            if (parent.value !== null && parent.value !== ''){ selected_value = parent.value; }
            
            const child = document.getElementById(dependent.child_ref_id);
            const url = "/flaskuio/relationship_dropdown/" + dependent.child_db + "/" + dependent.child_sql + "/" + id + "_" + selected_value; 
            const options = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            };
            fetch(url, options)
            .then(function(response){
                response.json()
                .then(
                    function(data){
                        
                        let html = "";
                        for(let item of data){
                            html += "<option value='"+ item.id +"'>"+ item.name +"</option>";
                        }
                        child.innerHTML = html;
                        $("#" + dependent.child_ref_id).dropdown('clear');
                        $("#" + dependent.child_ref_id).val('').change();
                    }
                )
            })
            .catch(function(error) {
                child.innerHTML = "";
                $("#" + dependent.child_ref_id).dropdown('refresh');
            });
        }
    });
}

function load_relationship_dropdown_field_ajax(id, dependents = []) {    
    $("#" + id).dropdown({
        ignoreDiacritics: true,
        fullTextSearch: 'exact',
    });

    $("#" + id).change(function(){
        for(let dependent of dependents){
            
            let api_values = "";
            for(let ref of dependent.depend_on){
                let value = document.getElementById(ref).value;
                if(value !== null && value !== ''){
                    api_values += ref + "_" + value;
                }else{
                    api_values += ref + "_0";
                }
                api_values += "$$";
            }
            
            
            const url = "/flaskuio/relationship_dropdown/" + dependent.child_db + "/" + dependent.child_sql + "/" + api_values; 
            
            let xhr = new XMLHttpRequest();

            xhr.open("GET", url, true);

            xhr.onprogress = function(){
                $("#" + dependent.child_ref_id).html("<option>Loading...</option>");
            }

            xhr.onreadystatechange = function(){
                if(this.readyState == 4){
                    if(this.status == 200){
                        let data = JSON.parse(this.responseText);
                        let output = "";
                        for(let i in data){
                            output += "<option value='"+ data[i].id +"'>"+ data[i].name +"</option>";
                        }
                        $("#" + dependent.child_ref_id).html(output);
                        $("#" + dependent.child_ref_id).dropdown('clear');
                        $("#" + dependent.child_ref_id).val('').change();
                    }else{
                        $("#" + dependent.child_ref_id).html("");
                        $("#" + dependent.child_ref_id).dropdown('clear');
                        $("#" + dependent.child_ref_id).val('').change();
                    }
                }
            }         
            
            xhr.onerror = function(){
                $("#" + dependent.child_ref_id).html("<option>Something went wrong!</option>");
            }

            xhr.send();

        }
    });
}

function load_modal(button_id, modal_id){
    $("#" + button_id).click(function(){
        $("#" + modal_id).modal('show');
    });
}