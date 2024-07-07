$(document).ready(function() {
    
    // get list of ingredients and populate search bar
    $('.search').on('click', async function(event) {
        event.preventDefault()
        console.log('hello')
       
        try {
            const[resp1, resp2] = await Promise.all([
                axios.get('/get_ingredients'),
                axios.post('/save_ingredients')])
                
            ingredients = new Ingredients(extractJson(resp1))

            console.log('resp from getting ingredients', resp1)
            console.log('resp from saving ingredients', resp2)

            populateSearchDropdown(ingredients)
            
        } catch(error) {
            console.log('Error', error)
        }
    })

    // hide dropdown when click happens elsewhere
    $(document).on('click', function(event) {
        if (!$(event.target).closest('.search-container').length) {
            $('#dropdown').hide()
        }
    })

    // obtain search query and pass into filterDropdown
    $('.search').on('input', function() {
        const query = $(this).val().trim()
        if (query == '') {
            $('dropdown').hide()
        }
        else {
            filterDropdown(query)
        }
    })


    // handle ingredient selection
    $('#dropdown').on('click', '.dropdown-item', function() {
        
        $(this).toggleClass('bg-info')
        const selectedIngredient = $(this).data('ingredient')
        toggleIngredientSelection(selectedIngredient)
    })



    // extracts the ingredients array from the json response
    function extractJson(response) {

        ingredientArray = response.data.ingredients
        return ingredientArray
    }

    // creates ingredient elements and populates the dropdown with them
    function populateSearchDropdown(ingredients){
        
        $('#dropdown').empty()
        ingredients = ingredients.ingredients.sort()
        for (const ingredient of ingredients) {
            $('#dropdown').append(`<a class="dropdown-item" href="#" data-ingredient="${ingredient}">${ingredient}</a>`)
        }
        $('#dropdown').show()
    }

    // filters the dropdown results based on user input
    function filterDropdown(query) {
        let hasVisibleItems = false
        $('#dropdown').find('.dropdown-item').each(function() {
            const item = $(this)
            const itemText = item.text().toLowerCase()
            if (itemText.includes(query.toLowerCase())) {
                hasVisibleItems = true
                $(this).show()
            }
            else {
                $(this).hide()
            }
        })

        if (hasVisibleItems == false) {
            $('#dropdown').hide()
        }
        else {
            $('#dropdown').show()
        }
    }


    // toggle ingredient selection
    function toggleIngredientSelection(ingredient) {
        
        something = $('#selected').find(`li[data-ingredient="${ingredient}"]`)
        console.log(something)
        let isSelected = $('#selected').find(`li[data-ingredient="${ingredient}"]`).length > 0

        if (isSelected) {
            $(`#selected li[data-ingredient="${ingredient}"]`).remove()
        }
        else {
            $('#selected').append(`<li class="list-group-item" data-ingredient="${ingredient}">${ingredient}</li>`)
        }

    }

})


// class to define each ingredient
class Ingredients {

    constructor(ingredients) {
        this.ingredients = ingredients
    }

}




 