var engine = new Bloodhound({
    remote: {
        url: the_ac_url,
        prepare: function (query, settings) {
            settings = settings.url + '?q=' + query;
            return settings;
        },
        transform: function (response) {
            return response.results;
        },
        rateLimitWait: 400
    },
    identify: function (obj) {return obj.id},
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    datumTokenizer: function (obj) {
        return Bloodhound.tokenizers.whitespace(obj.name);
    }
});

function suggestionTpl (obj) {
    var type;
    switch (obj.type) {
    case "mix":
    case "con":
        type = "Empresa";
        break;
    case "per":
        type = "Persona";
        break;
    }
    return '<div><strong>' + obj.name + '</strong> <small>- ' + type + '<small></div>';
}

function config_typeahead(){
    $('#input-company').typeahead(
        {
            highlight: false,
            hint: true,
            minLength : 2
        },
        {
            name: 'legalentities',
            limit: 100,
            source: engine,
            display: function (obj) {return obj.name},
            templates: {
                suggestion: suggestionTpl
            }
        });
}
