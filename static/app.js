alert("This is JS Speaking!");
// const BASE_URL = "http://localhost:5000/api";
// const form=document.getElementById("cupcake-add-form");
// const getCupcakesBtn=document.getElementById("getcupcakesbtn");

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

// // Passes form values to the api to create a new cupake. Takes in form data as parameters, submits to api/db and rerenders all cupcakes to the DOM. Called when the cupcake-add-form is submitted.
// async function createCupcake(flavor,image,rating,size){
//     const response=await axios.post("/api/cupcakes", {
// 		"flavor": `${flavor}`,
// 		"image": `${image}`,
// 		"rating": `${rating}`,
// 		"size": `${size}`
// 	})
//     console.log("this is the repsonse from create cupcake..." ,response);
//     const data=response.data;
//     console.log("this the create cupcake data...",data);
//     renderCupcakes()
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