

alert("Working JavaScript")

document.querySelector(".button").addEventListener('click',async()=>{


    let YoutubeLink=document.getElementById("Yt-Link").value

    let Circle_loading=document.querySelector(".loading-section")
  
    let Blog_content=document.querySelector(".Blog-Section")


    if (YoutubeLink)
    {

        Circle_loading.style.display="block"

        // Circle_loading.classList.remove("hidden")
        // console.log(Circle_loading)

        Blog_content.innerHTML=""


        const endpointurl="/generate-blog"


        try{

                // endpointurl=serveradress

                let response= await fetch(endpointurl,{
                    // fetch() → sends HTTP request to server
                    // await → waits for response

                    method:'POST',
                    // method: POST  means---Sending data to server (not just getting data).

                    headers:
                    {
                        'Content-Type':'application/json'
                    },

                    body: JSON.stringify({link:YoutubeLink})
                    // body = actual data you send to server
                    // JSON.stringify() → converts JavaScript object → JSON.
                    // {link: YoutubeLink}  to {"link":"YoutubeLink"}
                })

                let GetData= await response.json()

                Blog_content.innerHTML=GetData.content
                Circle_loading.style.display="none"

            


            }

            
         catch(error){
            console.log("Error Occured:",error)
            alert("Something went wrong pls tyr again later.")
             Circle_loading.style.display="none"

        }

    }

    else{

        alert("Please enter a Youtubelink")
    }


    
});






