$(document).ready(function() {
    
    $('#search').on('click', async function(event) {
        event.preventDefault()
        console.log('hello')
       
        try {
            const[resp1, resp2] = await Promise.all([
                axios.get('/get_ingredients'),
                axios.post('/save_ingredients')])
                
            ingredients = new Ingredients(extractJson(resp1))

            console.log('resp from getting ingredients', resp1)
            console.log('resp from saving ingredients', resp2)
            console.log(ingredients)
            
        } catch(error) {
            console.log('Error', error)
        }
    })

})



class Ingredients {

    constructor(ingredients) {
        this.ingredients = ingredients
    }

}

function extractJson(response) {

    ingredientArray = response.data.ingredients
    return ingredientArray
}


 