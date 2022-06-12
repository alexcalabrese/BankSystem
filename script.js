var user= document.getElementById("userBankAccount").value;

function login() {
        document.getElementById("infohomepage").style.display="block";
        if (user.length != 20) {
            alert("Error! leng")
            window.location.reload;
        } else {
            let re = /[0-9A-Fa-f]{20}/g;

            if (re.test(user)) {
                // let account = getAccount();
                console.log(getAccount());
                
            } else {
                alert('invalid bank account');
                window.location.reload;
                
            }

            re.lastIndex = 0;
        }
        const tableAPI = 'https://api.agify.io/?name=alex';
        const tableBody = document.querySelector('tbody');
        fetch(tableAPI)
        .then((response) => response.json())
        .then((todos) => {
            const array = [];
            array.push(todos)
            let stringFieldAll = "";
            array.forEach(row => { stringFieldAll.concat(`<tr>
                <td>${row.id}</td> 
                <td>${row.account_to}</td>
                <td>${row.amount}</td>
                </tr>`
            )
                
            });
        tableBody.innerHTML = stringFieldAll
    })
        .catch(console.error);

    }
    


 //async function getAccount() {
    let url = 'https://api.agify.io/?name=alex'
     fetch(url)
         .then(response => response.json())
         .then(account =>
         
            console.log(account.age));
        
     
      
     
// //cccccccccccccccccccc

function reloadpage(){
    window.location.reload;
}

function gotoTranfer(){
    window.location.href ='/transfer.html';
}
//--------------------------------------------------------------------------------------
let senderBankAccount = document.getElementById("senderBankAccount").value;
   let rcvBankAccount = document.getElementById("RcvBankAccount").value; 
   let moneyTransfer = document.getElementById("statusTransfer").value; 

    function logintransfer(){
        if( senderBankAccount.length  != 20 & rcvBankAccount.length!=20 & moneyTransfer < 0.00){
            alert("Incorrect data");
            setTimeout("window.location.reload();", 1500);
        }
        else{
            let re = /[0-9A-Fa-f]{20}/g;
            if(re.test(senderBankAccount) & re.test(rcvBankAccount)){
                //passano tutti i controlli e quindi facciamo partire i dati al back-end
            }
            else{
                alert("Incorrect data");
                setTimeout("window.location.reload();", 1500);            }
        }
        

    }

    function logintransfer(){
        document.getElementById("statusTable").style.display="block";
        var url = "";
        //url dell API
        var xhr = new XMLHttpRequest();
        xhr.open("PATCH", url);
        
        xhr.setRequestHeader("Accept", "application/json");
        xhr.setRequestHeader("Content-Type", "application/json");
        
        xhr.onreadystatechange = function () {
           if (xhr.readyState === 4) {
              console.log(xhr.status);
              console.log(xhr.responseText);
           }};
        
        var data = `{
            "account_from": senderBankAccount,
            "account_to": rcvBankAccount,
            "amount": moneyTransfer
          
        }`;
        
        xhr.send(data);
        


    }
