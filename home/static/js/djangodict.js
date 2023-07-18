function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    let currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function (e) {
        let a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(0, val.length).toUpperCase() === val.toUpperCase()) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");
                /*make the matching letters bold:*/
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                b.addEventListener("click", function (e) {
                    /*insert the value for the autocomplete text field:*/
                    inp.value = this.getElementsByTagName("input")[0].value;
                    /*close the list of autocompleted values,
                    (or any other open lists of autocompleted values:*/
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function (e) {
        let x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        /*If the TAB key is pressed*/
        if (e.keyCode === 9) {
            closeAllLists();
        }
        if (e.keyCode === 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode === 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode === 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (let i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        let x = document.getElementsByClassName("autocomplete-items");
        for (let i = 0; i < x.length; i++) {
            if (elmnt !== x[i] && elmnt !== inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
        // return document.getElementById(inp).value
    });
}

let opened_edit_buttons
let opened_symbol

function toggle_edit_buttons() {
    $('.edit_toggle').off('click').on('click', function () {
        console.log('edit toggled', $(this))
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
    $.get('?entry_id=' + entryID + '?entry_id', function (data) {
        console.log(data)
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
        console.log(data)
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
    get_and_append_page(page).done(function(data){
        page += 1
        // console.log('in done, next page', page)
        if (page <= number_of_pages){
            loopPages(page, number_of_pages)
        }
        toggle_edit_buttons()
    });
}
