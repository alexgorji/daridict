let currentFocus = -1;

function autocomplete(inp, language) {
    /*inp: text field element for each language */
    inp.on("input", function () {
        let value = inp.val()
        $.get('', {'language': language, 'autocomplete': value}, function (data) {
            $('#' + language + '_value_autocomplete').children().replaceWith(data);
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

    inp.on("keydown", function (e) {
        console.log(e.keyCode)
        const x = document.getElementById(this.id + "_autocomplete");
        if (e.keyCode === 9) {
            closeAllLists();
        } else if (e.keyCode === 40) {
            /*If the arrow DOWN key is pressed, increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode === 38) {
            /*If the arrow UP key is pressed, decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode === 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            const items = x.querySelectorAll('.autocomplete-item')
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (items) items[currentFocus].click();
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
    $('.edit_toggle').off('click').on('click', function () {
        // console.log('edit toggled', $(this))
        const target_buttons = $("#" + $(this).attr('data-buttons'));
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
                target_buttons.show()
                top_tr.addClass('top-tr')
                $(opened_symbol).removeClass('up');
                $(opened_symbol).addClass('right');
                $(opened_edit_buttons).removeClass('opened');
                $("#" + $(opened_edit_buttons).attr('data-buttons')).hide(500);
            } else {
                target_buttons.show(500)
                top_tr.addClass('top-tr')
            }
            opened_edit_buttons = this
            opened_symbol = symbol
            const that = this
            setTimeout(function () {
                $(".main-table-wrapper").animate({
                    scrollTop: $(that).closest('tr').position().top - 55
                }, 300);
            }, 500);
        }
    });
}

function createInput(id, value, type) {
    const edit_inputs_div_element = document.getElementById("data-editInputs");
    for (let i = 0; i < edit_inputs_div_element.children.length; ++i) {
        let child = edit_inputs_div_element.children[i];
        if (child.id === id) {
            return
        }
    }
    const new_input = document.createElement("input");
    new_input.setAttribute("type", type);
    new_input.setAttribute("class", "edit_button");
    new_input.setAttribute("id", id);
    new_input.setAttribute("name", id);
    new_input.setAttribute("value", value);
    edit_inputs_div_element.appendChild(new_input);
    return new_input
}

function createCancelInput() {
    const button_input = createInput("cancelButton", "CANCEL", "button")
    if (button_input) {
        button_input.onclick = function () {
            cancel();
        };
    }
}

let highlightedRow = null

function writeEntryItemsToFields(entryID, caller) {
    $.get('?entry_id=' + entryID, function (data) {
        // console.log(data)
        $('#entry_form').children().replaceWith(data);
    })
    // $.get('?page=' + page, function (data) {
    //     if (data != '') {
    //         $('#entries').append(data);
    //     } else {
    //         console.log("No data in page", page)
    //     }
    // });
    // console.log($(caller.closest('tr')).prev())

    //     $('#id_input_fields_button').trigger("click");
    // }
    // let field;
    // let language;
    // const entries = getEntry(entryID)
    // const items = entries.fields['items']
    // const tags = nodes.fields['tags']
    //
    // for (let key in fields) {
    //     language = key;
    //     field = fields[key];
    //     let value = "";
    //     for (let index in items) {
    //         let x = dictPkItemsJson[items[index]]
    //         if (x[0] === language) {
    //             value = x[1];
    //         }
    //     }
    //     field.value = value;
    //     const tag_field = document.getElementById("id_tags")
    //     value = ""
    //     for (let index in tags) {
    //         value = tagsPkTagJson[tags[index]].join(', ')
    //     }
    //     tag_field.value = value;
    //
    // }
}

function prepareEditChild(entryID, caller) {
    writeEntryItemsToFields(entryID, caller)
    // removeEditChild("editInput")
    // removeEditChild("newInput")
    // removeEditChild("copyInput")
    // removeEditChild("cancelButton")
    // removeEditChild("editEntryId")
    // if (highlightedRow) {
    //     highlightedRow.removeAttribute("class")
    // }
    // highlightedRow = caller.closest('tr');
    // highlightedRow.setAttribute("class", "highlight")

}

function editClick(entryID, caller) {

    $.get('', {'entry_id': entryID, 'edit': 'edit'}, function (data) {
        // console.log(data)
        $('#entry_form').children().replaceWith(data);
    })
    // prepareEditChild(entryId, caller)
    // createInput("editEntryId", entryId, "hidden")
    // createInput("editInput", "SAVE", "submit")
    // createCancelInput()
}

// function showInput(myname){
//     const myinput = $(input[name = myname])
//     myinput.removeClass('hide')
// }

function cancelClick() {
    console.log('cancelling')
    $.get('', {'cancel': 'cancel'}, function (data) {
        $('#entry_form').children().replaceWith(data);
    })
}

function copyClick(entryID, caller) {
    // console.log('copyClick', entryId)

    $.get('', {'entry_id': entryID, 'copy': 'copy'}, function (data) {
        $('#entry_form').children().replaceWith(data);
    })
    // const saveButton = $("input[name = entry-save]");
    // console.log(saveButton)
    // createInput("editEntryId", entryId, "hidden")
    // createInput("editInput", "SAVE", "submit")
    // createCancelInput()
}

function get_and_append_page(page) {
    return $.get('?page=' + page, function (data) {
        if (data != '') {
            $('#entries').append(data);
        } else {
            console.log("No data in page", page)
        }
    });
}

function loopPages(page, number_of_pages) {
    get_and_append_page(page).done(function (data) {
        page += 1
        // console.log('in done, next page', page)
        if (page <= number_of_pages) {
            loopPages(page, number_of_pages)
        }
        toggle_edit_buttons()
    });
}
