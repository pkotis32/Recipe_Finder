$(document).ready(function() {
    
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

    $(document).on('click', function(event) {
        if (!$(event.target).closest('.search-container').length) {
            console.log('hello')
            $('#dropdown').hide()
        }
    })

    $('.search').on('input', function() {
        console.log('change')
        const query = $(this).val().trim()
        if (query == '') {
            $('dropdown').hide()
        }
        else {
            filterDropdown(query)
        }
    })


    function extractJson(response) {

        ingredientArray = response.data.ingredients
        return ingredientArray
    }


    function populateSearchDropdown(ingredients){
        
        $('#dropdown').empty()
        ingredients = ingredients.ingredients.sort()
        for (const ingredient of ingredients) {
            $('#dropdown').append(`<a class="dropdown-item" href="#">${ingredient}</a>`)
        }
        $('#dropdown').show()
    }

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
    }

})



class Ingredients {

    constructor(ingredients) {
        this.ingredients = ingredients
    }

}




 