alert("This is JS Speaking!");
const BASE_URL = "http://localhost:5000/api";

// Jquery Selectors
const $guessForm=$("#guessform");
const guessForm=document.getElementById("guessform")
const hiveText=document.getElementsByClassName("text-dark")
const hives=document.getElementsByClassName("hive")
const hive1=$("#hive1");
const $guessInput=$("#guess")
const $messageContainer=$("#messagecontainer")
const ratingContainer=$("ratingcontainer")
const $scoreContainer=$("scorecontainer")
const $guessedWordsContainer=$("#guessed_words_container")

console.log(`this is guessInput--->${$guessInput}`)
console.log(`this is hiveText---->${hiveText}`)
console.log(`this is hives---->${hives}`)

// sends form guess form word to the server for validation.Receives response an
async function checkWord(){
    // word is forced to uppercase because words list is formatted in all caps. We are just fixing this for the user before any issue can occur.
    const word=$('#guess').val().toUpperCase()
    const response=await axios.post("/spellingbee/validate", {
		"word": `${word}`,
	})
    console.log("this is the repsonse from spellingbee/validate..." ,response);
    const data=response.data;
    console.log("this the response data...",data);
    console.log(data.score)
    console.log(data.result)
    console.log(data.guessed_words)
    displayScoreRating(data.score, data.rating)
    displayGuessMessage(data.result)
    displayRating(data.rating)
    displayGuessedWords(data.guessed_words)
    return data
    
}

function displayGuessMessage(result){
    if (result === "valid"){
        $messageContainer.empty()
        $messageContainer.append(`<h2 class="message fade-out">  &#128029 ${result} </h2>`)
    }
    else{
    $messageContainer.empty()
    $messageContainer.append(`<h2 class="message fade-out"> ${result}</h2>`)}
}
//Displays current score of the user in the DOM
function displayScoreRating(score,rating){
    $("#scorecontainer").empty()
    $("#scorecontainer").append(`<h3 class="score"> Current Score:${score}</h3>`)

    if (rating === "Genius"){
    $("#scorecontainer").append(`<h3 class="rating"> Current rating: &#127891 &#127891 ${rating}</h3>`)}

    else if(rating ==="Amazing"){
    $("#scorecontainer").append(`<h3 class="rating"> Current rating: &#127891 ${rating}</h3>`)}

    else if(rating ==="Great"){
    $("#scorecontainer").append(`<h3 class="rating"> Current rating: &#128029 &#128029 &#128029 ${rating}</h3>`)}

    else if(rating ==="Nice"){
    $("#scorecontainer").append(`<h3 class="rating"> Current rating: &#128029 &#128029 ${rating}</h3>`)}

    else if(rating ==="Solid"){
        $("#scorecontainer").append(`<h3 class="rating"> Current rating: &#128029  ${rating}</h3>`)}
    
    else{
        $("#scorecontainer").append(`<h3 class="rating"> Current rating: ${rating}</h3>`)
    }}


function displayRating(rating){
    $("#ratingcontainer").empty()
    $("#ratingcontainer").append(`<li class="rating"> Rating:${rating}</li>`)
}

function displayGuessedWords(guessedWords){
    $("#guessed_words_container").empty()
    const lenGuessedWords=guessedWords.length
    const h3template=`<h3>you have found ${lenGuessedWords} words</h3>`
    $("#guessed_words_container").append(h3template)
    sorted=guessedWords.sort()
    for(let word of sorted){
        $("#guessed_words_container").append(`<li class="foundword">${word}</li>`)
    }
}

function hideGameComponents(){
    $("#gameboardcontainer").hide()
    $("#gameinfocontainer").hide()
}

function showGageComponents(){
    $("#gameboardcontainer").show()
    $("#gameinfocontainer").show()
}

$("#hive1").click(function (){
    const letter=$("#hive1").text()
    console.log(`clicked! you are inside hive1 evt listener! here is the letter ${letter}`)
    $("#guess").append(letter)
} )

$("#togglebutton").click(function(){
    console.log("clicked! inside the toggle button evt listener" )
    $("#guessed_words_container").toggle()
})

$("#togglebuttonrules").click(function(){
    console.log("clicked! inside the button toggle evt listener for game rules" )
    $("#rulescontainer").toggle()
})

$("#togglebuttonruleshints").click(function(){
    console.log("clicked! inside the button toggle evt listener for game rules in the hints page" )
    $("#rulescontainerhints").toggle()
})

$("#togglebuttonglossary").click(function(){
    console.log("clicked! inside the button toggle evt listener for the glossary in the hints page" )
    $("#hintsglossarycontainer").toggle()
})


$("#guessdeletebtn").click(function(){
    console.log("clicked insinde the guessdeletebtn evn listner")
    $("#guess").val("")
})


// evt listener which handles form submission of a new cupcake to the api. Also invokes renderCupcakes() to load the new cupcake to the DOM 
guessForm.addEventListener('submit', async function (evt){
    const word=$('#guess').val()
    evt.preventDefault();
    console.log('clicked',"the evt listener is working", "inside guessform evt listener")
    console.log(".....................................")
    console.log(`this is the guessword from the form ${word}`)
    await checkWord()
    $('#guess').val("")
})





// function hidePageComponents() {
//     const components = [
//       $allStoriesList,
//       $loginForm,
//       $signupForm,
//       $newStoryForm,
//       $favoritedStoriesList,
//       $myStoriesList,
//       $userProfile,
//     ];
//     components.forEach(c => c.hide());// hide is a jQuery function that hides the component, but this is fancy! here we put each component as a jQuery item already and just called hide on it
//   }
  





// hiveText.addEventListener("click", function(evt){
//     const letter=evt.target.val()
//     console.log(`${letter} was pressed`) 
// })


// // Fetches all cupcakes in the api, returns that data as a list of objects called cupcakes. Utilized by renderCupcakes().
// async function getCupcakes(){
//     const response=await axios.get("/api/cupcakes")
//     console.log("this is the repsonse...Inside GetCupcakes" ,response);
//     const data=response.data;
//     console.log("this is data...",data);
//    const cupcakes=data.cupcakes;
//     console.log("this is cupcakes...",cupcakes);
//     return cupcakes;
// }

// //  Utilizes api data from getCupcakes(), interates over each cupcake object rendering the data into html with bootstrap class formatting. Can also do it without, see commented out code.
// // Called when user clicks get the get cupcakes button via axios btn and when the cupcake-add-form is submitted.
// async function renderCupcakes(){
//     // this line isn't needed because getCupcakes will give you cupcakes anyways, but just being explicit. CUPCAKES.
//    const cupcakes=await getCupcakes()
//     console.log("this is what cupcakes is from inside renderCupcakes.....",cupcakes)
//     $("#cupcakediv").empty() 
//     for (let cupcake of cupcakes){
//         // $("#cupcakelist").append(`<div class=cupcakewrapper><img class=image src=${cupcake.image} width="200" height="300" ><li><b>Flavor:</b>${cupcake.flavor}, <b>Rating:</b> ${cupcake.rating},<b>Size:</b> ${cupcake.size}</li></div>`) Just some original formatting logic before integrationg of bootstrap formatting in the JS
//         $("#cupcakediv").append(`<div class="col-sm-2">
//         <img class="img-thumbnail" src=${cupcake.image} alt=" RIP cupcake image was supposed to go here">
//         <p class="text-info font-italic"><b>Flavor:</b> ${cupcake.flavor}</p>
//         <p class="text-info font-italic "><b>Rating:</b> ${cupcake.rating}</p>
//         <p class="text-info font-italic "><b>Size:</b> ${cupcake.size}</p>
//     </div> `)
//     }
// }


// // evt listener which handles form submission of a new cupcake to the api. Also invokes renderCupcakes() to load the new cupcake to the DOM 
// form.addEventListener('submit', async function (evt){
//     evt.preventDefault();
//     const flavor=$('#flavor').val()
//     const image=$('#image').val()
//     const rating=$('#rating').val()
//     const size=$('#size').val()
//     console.log('clicked',"the evt listener is working", "inside guessform evt listener")
//     console.log(".....................................")
//     console.log("this is what word the form will send....",`the flavor is... ${flavor} the image is ${image} the rating is ${rating} the size is ${size}`)
//     await createCupcake(flavor,image,rating,size)
//     $('#flavor').val("")
//     $('#image').val("")
//     $('#rating').val("")
//     $('#size').val("")})


// // button with evt listener which will also render cupcakes to the dom
// getCupcakesBtn.addEventListener("click", renderCupcakes)

// // Start the application.
// document.addEventListener("DOMContentLoaded",renderCupcakes)




// $( "#cupcake-add-form" ).on('submit', async function (evt){
//     evt.preventDefault();
//     const flavor=$('#flavor').val()
//     const image=$('#image').val()
//     const rating=$('#rating').val()
//     const size=$('#size').val()
//     console.log('clicked',"the evt listener is working", "inside guessform evt listener")
//     console.log(".....................................")
//     console.log("this is what word the form will send....",`the flavor is... ${flavor} the image is ${image} the rating is ${rating} the size is ${size}`)

//     await createCupcake(flavor,image,rating,size)
//     $('#flavor').val("")
//     $('#image').val("")
//     $('#rating').val("")
//     $('#size').val("")})