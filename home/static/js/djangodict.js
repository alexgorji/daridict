let currentFocus = -1;

function autocomplete(inp, language) {
    /*inp: text field element for each language */
    inp.on("input.entry-form", function () {
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

function editClick(entryID) {
    $.get('', {'entry_id': entryID, 'edit': 'edit'}, function (data) {
        // console.log(data)
        $('#entry_form').children().replaceWith(data);
    });
}

function cancelClick() {
    console.log('cancelling')
    $.get('', {'cancel': 'cancel'}, function (data) {
        $('#entry_form').children().replaceWith(data);
    })
}

function copyClick(entryID) {

    $.get('', {'entry_id': entryID, 'copy': 'copy'}, function (data) {
        $('#entry_form').children().replaceWith(data);
    })
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