function add_input_search(number){
    var id= 'input-q_' +  number.toString()
    var sibling = $("div.search-input").last();
    var content = '<div class="form-group search-input">\n' +
        '<label class="control-label col-sm-2" for="input-q_' + number.toString() +
        '">&nbsp;O&nbsp;</label>\n' +
        '<div class="col-sm-10">\n' +
        '<input type="text" id="' +  id +
        '" size="30" class="form-control"' +
        'autocomplete="off" spellcheck="false"' +
        'placeholder="Otro término de búsqueda" autofocus\n' +
        'name="q_' + number.toString()+ '"></input>\n' +
        '</div> ';
    sibling.after(content);
    $('#' + id).focus();
}

function init_add_input_search(){
    var input_number = 0;
    $('#bt-synonym').click('', function() {
        input_number += 1;
        add_input_search(input_number);
    });
}

function is_checked(party){
    // parties defined in search.html
    return (parties.length == 0)
        || parties.indexOf(party) != -1; // -1 is not found
}

function update_parties(){
    var parties = zones[$('#zone').val()].parties;
    var html = "";
    for (var i = 0; i < parties.length; i++) {
        html += '<div class="checkbox col-sm-3 col-xs-4"><label>';
        html += '<input class="party-check" value="' + parties[i] + '" type="checkbox"';
        if (is_checked(parties[i]))
            html += ' checked';
        html += '> ';
        // html += programs[parties[i]][1] + '</label></div>';
        html += '<img  width="60" height="60" alt="' + programs[parties[i]][1];
        html += '" src="'+ static_img + programs[parties[i]][0] + '.png"></img>';
        html += '</label></div>';
    }
    $('#parties-container').html(html);
}

function update_parties_change(){
    // parties defined in search.html
    parties = [];
    update_parties();
}

function update_party_input(){
    var parties = [];
    $(".party-check").each(function (){
        console.log(this.checked)
        if (this.checked)
            parties.push(jQuery(this).val());
    });
    $('#parties').val(parties.join(','));
    return true;
}

function init_zone_select(){
    $('#zone').change(update_parties_change);
    $('#button-submit').click(update_party_input);
    update_parties();
}

$(document).ready(function () {
    init_add_input_search();
    init_zone_select();
});
