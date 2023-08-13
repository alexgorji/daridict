let currentFocus = -1;

function autocomplete(inp, autocompleteFieldId, tags = false, language) {
    /*inp: text field element for each language */
    if (tags === true) {
        inp.on("input", function () {
            let tags_as_string = inp.val()
            let array_of_tags = tags_as_string.split(', ')
            $.get('', {'autocompletetags': tags_as_string}, function (data) {
                $('#' + autocompleteFieldId).children().replaceWith(data);
                /*make the matching letters bold*/
                /*on click for matched word*/
                $(".autocomplete-item").map(function () {
                    // this.innerHTML = '<strong>' + this.innerText.slice(0, value.length) + '</strong>' + this.innerText.slice(value.length);
                    this.addEventListener("click", function (e) {
                        if (array_of_tags.slice(0, -1).length > 0) {
                            inp.val(array_of_tags.slice(0, -1).toString() + ', ' + this.innerText)
                        } else {
                            inp.val(this.innerText)
                        }

                        closeAllLists();
                    });
                });
            });
        });
    } else {
        inp.on("input", function () {
            let value = inp.val()
            $.get('', {'language': language, 'autocomplete': value}, function (data) {
                // $('#' + language + '_value_autocomplete').children().replaceWith(data);
                $('#' + autocompleteFieldId).children().replaceWith(data);
                /*make the matching letters bold*/
                /*on click for matched word*/
                $(".autocomplete-item").map(function () {
                    this.innerHTML = '<strong>' + this.innerText.slice(0, value.length) + '</strong>' + this.innerText.slice(value.length);
                    this.addEventListener("click", function (e) {
                        inp.val(this.innerText)
                        closeAllLists();
                    });
                });
            });
        });
    }
    inp.on("keydown", function (e) {
        // console.log(e.keyCode)
        // const x = document.getElementById(this.id + "_autocomplete");
        const x = document.getElementById(autocompleteFieldId);

        if (e.keyCode === 9) {
            closeAllLists();
        } else if (e.keyCode === 40) {
            /*If the arrow DOWN key is pressed, increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
            const position = currentFocus * 24;
            $('.autocomplete-active').closest('.autocomplete').scrollTop(position)
        } else if (e.keyCode === 38) {
            /*If the arrow UP key is pressed, decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
            const position = currentFocus * 24;
            $('.autocomplete-active').closest('.autocomplete').scrollTop(position)
        } else if (e.keyCode === 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            const items = x.querySelectorAll('.autocomplete-item')
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (items) items[currentFocus].click();
            } else {
                $('.search-button').click()
            }
        }
    });

    function closeAllLists() {
        $(".autocomplete-items").map(function () {
            $(this).empty()
        });
        currentFocus = -1
    }

    function addActive(x) {
        const items = x.querySelectorAll('.autocomplete-item')
        /*a function to classify an item as "active":*/
        if (!items) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);

        if (currentFocus >= items.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (items.length - 1);
        /*add class "autocomplete-active":*/
        items[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        const items = x.querySelectorAll('.autocomplete-item')
        for (let i = 0; i < items.length; i++) {
            items[i].classList.remove("autocomplete-active");
        }
    }

    document.addEventListener("click", function () {
        closeAllLists();
    });
}

let opened_edit_buttons
let opened_symbol

function toggle_edit_buttons() {
    $('.edit_toggle').off().on('click', function () {
        const id = $(this).closest('tr').attr('id')
        const target_buttons = $('tr[data-for-entry=' + id + ']').find('div')
        const top_tr = $(this).closest('tr')
        const symbol = $(this).children("i").first()

        if ($(this).hasClass('opened')) {
            $(symbol).removeClass('up')
            $(symbol).addClass('right')
            $(this).removeClass('opened')
            target_buttons.hide(500)
            top_tr.removeClass('top-tr')
            opened_edit_buttons = null
            opened_symbol = null
        } else {
            $(this).addClass('opened')
            $(symbol).removeClass('right')
            $(symbol).addClass('up')

            if (opened_edit_buttons) {
                target_buttons.show(500)
                top_tr.addClass('top-tr')
                $(opened_symbol).removeClass('up');
                $(opened_symbol).addClass('right');
                $(opened_edit_buttons).removeClass('opened');
                $(opened_edit_buttons).closest('tr').removeClass('top-tr');
                $('tr[data-for-entry=' + $(opened_edit_buttons).closest('tr').attr('id') + ']').find('div').hide(500)
            } else {
                target_buttons.show(500)
                top_tr.addClass('top-tr')
            }
            opened_edit_buttons = this
            opened_symbol = symbol
            // const that = this
            // setTimeout(function () {
            //     $(".main-table-wrapper").animate({
            //         scrollTop: $(that).closest('tr').position().top - 55
            //     }, 300);
            // }, 500);
        }
    });
}

function editClick(entryID) {
    $.get('', {'entry_id': entryID, 'edit': 'edit'}, function (data) {
        $('#id-entry-form').children().replaceWith(data);
        loadAutocompletions();
        saveUpdateButtons()
    });
}

function cancelClick() {
    console.log('cancelling')
    $.get('', {'cancel': 'cancel'}, function (data) {
        $('#id-entry-form').children().replaceWith(data);
        loadAutocompletions();
        saveUpdateButtons()
    })
}

function copyClick(entryID) {

    $.get('', {'entry_id': entryID, 'copy': 'copy'}, function (data) {
        $('#id-entry-form').children().replaceWith(data);
        loadAutocompletions();
        saveUpdateButtons()

    })
}

function getAndAppendPage(page, get_parameters) {
    let all_get_parameters = null
    if (get_parameters) {
        all_get_parameters = get_parameters + '&page=' + page
    } else {
        all_get_parameters = '?page=' + page
    }
    return $.get(all_get_parameters, function (data) {
        if (data != '') {
            $('#entries').append(data);
        } else {
            console.log("No data in page", page)
        }
    });
}

function loopPages(page, number_of_pages, get_parameters) {
    getAndAppendPage(page, get_parameters).done(function (data) {
        page += 1
        // console.log('in get_and_append_page done, next page', page)
        if (page <= number_of_pages) {
            loopPages(page, number_of_pages, get_parameters)
        }
        toggle_edit_buttons()
        $(function () {
            $('.tag-button').popover()
            $('.comment-button').popover()
        })
    });
}

function loadAutocompletions() {
    let fields = {
        'german': $("#id_german-value"),
        'farsi': $("#id_farsi-value"),
        'dari': $("#id_dari-value"),
    }

    let language;
    let field;
    for (let key in fields) {
        language = key;
        field = fields[key];
        autocomplete(field, "id_" + language + "-value_autocomplete", false, language);
    }
    autocomplete($('#id_search_field'), "id_search_field_autocomplete", false, null);
    autocomplete($('#id_tag_names'), "id_tag_names_autocomplete", true);
    autocomplete($('#id_tag_search_field'), "id_tag_search_autocomplete", true);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function convertFormToJSON(form) {
    const array = $(form).serializeArray(); // Encodes the set of form elements as an array of names and values.
    const json = {};
    $.each(array, function () {
        json[this.name] = this.value || "";
    });
    return json;
}


function saveUpdateButtons() {
    $('button[name = "entry-update"]').on('click', function () {
        const csrftoken = getCookie('csrftoken');
        const dari_value = $("#id_dari-value").val()
        const farsi_value = $("#id_farsi-value").val()
        const german_value = $("#id_german-value").val()
        const tag_names = $('#id_tag_names').val()
        const entry_id = $(this).attr('data-entry-id')
        console.log('update clicked', entry_id)
        $.post('', {
            'dari_value': dari_value,
            'farsi_value': farsi_value,
            'german_value': german_value,
            'tag_names': tag_names,
            'selected_entry_id': entry_id,
            'entry-update': 'yes',
            'csrfmiddlewaretoken': csrftoken
        }, function (data) {
            // console.log($("#id_entry_"+entry_id).find($('.entry-tags')))
            // $("#id_entry_"+entry_id).replaceWith(data)
            let td_elements = $("#id_entry_" + entry_id).children()
            for (let i = 2; i < td_elements.length; ++i) {
                td_elements[i].remove()
            }
            $("#id_entry_" + entry_id).append(data)
            $("#id_entry_" + entry_id).find($('[data-toggle="popover"]')).popover()
        });
    });
    $('button[name = "entry-save"]').on('click', function () {
        const csrftoken = getCookie('csrftoken');
        const dari_value = $("#id_dari-value").val()
        const farsi_value = $("#id_farsi-value").val()
        const german_value = $("#id_german-value").val()
        const tag_names = $('#id_tag_names').val()
        console.log('save clicked', $(this).attr('data-entry-id'))
        $.post('', {
            'dari_value': dari_value,
            'farsi_value': farsi_value,
            'german_value': german_value,
            'tag_names': tag_names,
            'entry-save': 'yes',
            'csrfmiddlewaretoken': csrftoken
        }, function (data) {
            if (data) {
                $('.my-table').find('tbody').prepend(data);
                toggle_edit_buttons();
                $('.table-wrapper').animate({
                    scrollTop: 0
                }, 300)
            }
        });
    });
}