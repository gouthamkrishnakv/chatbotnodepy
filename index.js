const express = require('express')
const ejs = require('ejs')
const fs = require('fs')
const app = express()
const bodyParser = require('body-parser')


app.set('view engine', 'ejs')
app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json())

app.get('/',(_req,res)=>{
    fs.writeFile('responses.json',JSON.stringify({}),(err)=>{
        if(err){
            res.render('index',{title: 'Node Chatbot', heading: 'Error, Please sanitize the files.'})
        }
        else{
            res.render('index',{title: 'Node Chatbot', heading: 'Node Chatbot'})
        }
    })
})

app.post('/',(req,res)=>{
    console.log(req.body.query);
    var exec = require('child_process').exec;
    fs.writeFile('question.qn',req.body.query,(err)=>{
        if(err){
            throw err;
        }
        else{
            const filename = 'file.json'
            // console.log('./main.py ' + 'file.json ' + 'question.qn')
            exec(`python main.py ${filename}`,(err,sout,sin)=>{
                if(err){
                    throw err;
                }
                else{
                    fs.readFile('./res.json',(err, data)=>{
                        if(err){
                            throw err;
                        }
                        else{
                            console.log(JSON.parse(data))
                        }
                    });
                }
            })
        }
    })
    res.send('RESPONSE FOUND')
})

app.get('file.json',(req,res)=>{
})


app.listen(4500,()=>{
    console.log('LISTENING AT PORT 4500')
})