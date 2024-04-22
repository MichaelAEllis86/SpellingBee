// alert("This is JS Speaking!");
// const BASE_URL = "http://localhost:5000/api";
const apiKey="13b41308-060f-495a-8411-8686570431a6"
const dictionaryapiurl="https://www.dictionaryapi.com/api/v3/references/collegiate/json/voluminous?key=your-api-key"

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
const $dictionaryForm=$("#dictionaryform")
const loginheader=document.getElementById("loginheader")

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
        $messageContainer.append(`<h3 class="message fade-out">  &#128029 ${result} </h3>`)
    }
    else if (result ==="pangram"){
        $messageContainer.empty()
        $messageContainer.append(`<h3 class="message fade-out">  &#127891 ${result} </h3>`)
    }
    else{
    $messageContainer.empty()
    $messageContainer.append(`<h3 class="message fade-out"> ${result}</h3>`)}
}
//Displays current score of the user in the DOM
function displayScoreRating(score,rating){
    $("#scorecontainer").empty()
    $("#scorecontainer").append(`<h3 class="score"> Current Score:${score}</h3>`)

    if (rating === "Genius"){
    $("#scorecontainer").append(`<h3 class="rating rowgenius"> Current rating: &#127891 &#127891 ${rating}</h3>`)}

    else if(rating ==="Amazing"){
    $("#scorecontainer").append(`<h3 class="rating rowamazing"> Current rating: &#127891 ${rating}</h3>`)}

    else if(rating ==="Great"){
    $("#scorecontainer").append(`<h3 class="rating rowgreat"> Current rating: &#128029 &#128029 &#128029 ${rating}</h3>`)}

    else if(rating ==="Nice"){
    $("#scorecontainer").append(`<h3 class="rating rownice"> Current rating: &#128029 &#128029 ${rating}</h3>`)}

    else if(rating ==="Solid"){
    $("#scorecontainer").append(`<h3 class="rating rowsolid"> Current rating: &#128029  ${rating}</h3>`)}
    
    else if(rating ==="Good"){
    $("#scorecontainer").append(`<h3 class="rating rowgood"> Current rating: ${rating}</h3>`)}

    else if(rating ==="movingup"){
        $("#scorecontainer").append(`<h3 class="rating rowmovingup"> Current rating: ${rating}</h3>`)}
    
    else if(rating ==="Good start"){
    $("#scorecontainer").append(`<h3 class="rating rowgoodstart"> Current rating: ${rating}</h3>`)}

    else if(rating ==="Beginner"){
        $("#scorecontainer").append(`<h3 class="rating rowbeginner"> Current rating: ${rating}</h3>`)}
    
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

function displayDictionaryWords(responseWordData,searchWord){
    $("#dictionarywordscontainer").empty()
    if (responseWordData[0].meta ===undefined){
       const nomatchesmsg=`<i class="rulesli"><b> your word (${searchWord})</b>was not found, please find closest matches below!</i>`
        $("#dictionarywordscontainer").append(nomatchesmsg)
        for(let word of responseWordData){
            $("#dictionarywordscontainer").append(`<p class="rulesli">${word}<p>`)
        }
    }
    else{
        if(responseWordData[0].hwi.prs!==undefined && responseWordData[0].hwi.prs[0].sound!==undefined ){
            let audiotag=`<audio controls src="https://media.merriam-webster.com/audio/prons/en/us/mp3/${searchWord[0]}/${responseWordData[0].hwi.prs[0].sound.audio}.mp3">pronunciation:</audio>`
            let messsagetag=`<p id=dictionarysearchresponse class="rulesli"> <b><i>Dictionary  entries for: ${searchWord}</i></b></p>`
            $("#dictionarywordscontainer").append(messsagetag,audiotag)}
        else{
           let messsagetag=`<p id=dictionarysearchresponse class="rulesli"> <b><i>Dictionary  entries for: ${searchWord}</i></b></p>`
            $("#dictionarywordscontainer").append(messsagetag)} 
        }
       
    for (let word of responseWordData){
        templatetag=`<p class="rulesli"><b>${searchWord}<i>(${word.fl})</i>-</b></p>`
        datetag=`<p class="rulesli"><i>date:(${word.date})</i></p>`
        $("#dictionarywordscontainer").append(templatetag,datetag)
        for (let def of word.shortdef){
        definition=`<p class="rulesli">${def}<p>`
        $("#dictionarywordscontainer").append(definition)}
        // for (let idx of word.et){
        //     etymologytag=`<p class="rulesli"><i>etymology::</i>${idx}<p>`
        // $("#dictionarywordscontainer").append(etymologytag)}

        }
        }

async function dictionarySearch(){
    const searchWord=$("#dictionarysearch").val()
    const response=await axios.get(`https://www.dictionaryapi.com/api/v3/references/collegiate/json/${searchWord}`,
    {params:{key:apiKey}})
    data=response.data
    console.log(data)
    displayDictionaryWords(data,searchWord)
}

function randomPurple(){
    const hexPurples=["#51087E","#6C0BA9","#880ED4","#A020F0","#B24BF3","#C576F6","#D7A1F9"]
    let randoPurp=_.sample(hexPurples)
    console.log(randoPurp)
    console.log(typeof randoPurp)
    return randoPurp
 }
 setInterval(function(){
    console.log(`this is the random purple inside set interval`)
    loginheader.style.color=`${randomPurple()}`
 },3000)

function hideGameComponents(){
    $("#gameboardcontainer").hide()
    $("#gameinfocontainer").hide()
}

function showGageComponents(){
    $("#gameboardcontainer").show()
    $("#gameinfocontainer").show()
}

// $("#hive1").click(function (){
//     const letter=$("#hive1").text()
//     console.log(`clicked! you are inside hive1 evt listener! here is the letter ${letter}`)
//     $("#guess").append(letter)
// } )

$("#togglebutton").click(function(){
    console.log("clicked! inside the toggle button evt listener" )
    $("#guessed_words_container").toggle()
})

$("#hintsnavbutton").click(function(){
    console.log("clicked! inside the hintsnavbutton toggle button evt listener" )
    $("#hintsgamepagecontainer").toggleClass("hidden")
    $("#guessed_words_container").toggleClass("hidden")
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
    console.log("clicked insinde the guessdeletebtn evt listner")
    $("#guess").val("")
})

$("#aboutbtn").click(function(){
    console.log("clicked insinde the aboutbtn evt listner")
    $("#aboutcontainer").toggle()
    $("#loginheaderscontainer").toggle()
})

$("#aboutclose").click(function(){
    console.log("clicked insinde the aboutbtn evt listner")
    $("#aboutcontainer").toggle()
    $("#loginheaderscontainer").toggle()
})

$( document ).ready(function() {
    $("#aboutcontainer").toggle()
  });

$("#signupbtn").click(function(){
    console.log("clicked insinde the signupbtn evt listner")
    $("#signupformcontainer").toggle()
    $("#loginheaderscontainer").toggle()
})

$("#signupclose").click(function(){
    console.log("clicked insinde the signupbtn evt listner")
    $("#signupformcontainer").toggle()
    $("#loginheaderscontainer").toggle()
})

// $("#loginbtn").click(function(){
//     console.log("clicked insinde the signupbtn evt listner")
//     $("#Loginformcontainer").toggle()
//     $("#loginheaderscontainer").toggle()
// })

// $("#loginclose").click(function(){
//     console.log("clicked insinde the signupbtn evt listner")
//     $("#Loginformcontainer").toggle()
//     $("#loginheaderscontainer").toggle()
// })


// 
guessForm.addEventListener('submit', async function (evt){
    const word=$('#guess').val()
    evt.preventDefault();
    console.log('clicked',"the evt listener is working", "inside guessform evt listener")
    console.log(".....................................")
    console.log(`this is the guessword from the form ${word}`)
    await checkWord()
    $('#guess').val("")
})

$dictionaryForm.on("submit",async function (evt){
    const searchWord=($("#dictionarysearch").val())
    evt.preventDefault();
    console.log('clicked',"the evt listener is working", "inside dictionaryform evt listener")
    console.log(`this is the searchWord from the form ${searchWord}`)
    await dictionarySearch()
    $("#dictionarysearch").val("")
})
