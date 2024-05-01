var mongoose = require('mongoose');
const fs = require("fs").promises;
var axios = require('axios');


var clientModel = require('./mongo/model/client'),
	tokenModel = require('./mongo/model/token'),
	userModel = require('./mongo/model/user');


     var loadExampleData = function() {

    //     var client1 = new clientModel({
    //         id: 'application',	// TODO: Needed by refresh_token grant, because there is a bug at line 103 in https://github.com/oauthjs/node-oauth2-server/blob/v3.0.1/lib/grant-types/refresh-token-grant-type.js (used client.id instead of client.clientId)
    //         clientId: 'application',
    //         clientSecret: 'secret',
    //         grants: [
    //             'password',
    //             'refresh_token'
    //         ],
    //         redirectUris: []
    //     });
    
    //     var client2 = new clientModel({
    //         clientId: 'confidentialApplication',
    //         clientSecret: 'topSecret',
    //         grants: [
    //             'password',
    //             'client_credentials'
    //         ],
    //         redirectUris: []
    //     });
    
        var user = new userModel({
            username: 'adi',
            password: 'password'
        });
    
    //     client1.save();
    
         user.save();
    
    //     client2.save();
     };
    // loadExampleData();

var getClient = function(clientId, clientSecret, callback) {
       clientModel.findOne({
            clientId: clientId,
            clientSecret: clientSecret
        }).lean().exec().then((function(callback, client) {
            if (!client) {
                console.error('Client not found');
            }
    
            callback(null, client);
        }).bind(null, callback));
    };


    var saveToken = function(token, client, user, callback) {

        token.client = {
            id: client.clientId
        };
    
        token.user = {
            username: user.username
        };
    
        var tokenInstance = new tokenModel(token);
        tokenInstance.save().then((function(callback, token) {
    
            if (!token) {
                console.error('Token not saved');
            } else {
                token = token.toObject();
                delete token._id;
                delete token.__v;
            }
    
            callback(null, token);
        }).bind(null, callback));
    };



    var getUser = function(username, password, callback) {

        
      
       
        userModel.findOne({
            username: username,
        }).lean().exec().then((function(callback, user) {
    
            if (!user) {
                console.error('User not found');
            }
            else{
                (async () => {
  
                    // string generated by canvas.toDataURL()
                    //const img = password;
                    const img = password;
                      
                    // strip off the data: url prefix to get just the base64-encoded bytes
                    const data = img.replace(/^data:image\/\w+;base64,/, "");
                    
                    const buf = Buffer.from(data, "base64");
                    await fs.writeFile( "./images/" +username+ ".png", buf);
                  })().then(async function (){
                    var data = {"username" : username};
                    const response = await axios.post("http://localhost:5001/verify",data);
        
                  console.log(response.data);
                  if(response.data.status == 'verified'){
                    callback(null,user);
                  }
                  else{
                    callback({error:"not verified"}, user);
                  }
                  });
            }
    
            
        }).bind(null, callback));
    };

    var getUserFromClient = function(client, callback) {

        clientModel.findOne({
            clientId: client.clientId,
            clientSecret: client.clientSecret,
            grants: 'client_credentials'
        }).lean().exec().then((function(callback, client) {
            
            if (!client) {
                console.error('Client not found');
            }
    
            callback(err, {
                username: ''
            });
        }).bind(null, callback));
    };


    module.exports = {
        // getAccessToken: getAccessToken,
        getClient: getClient,
        saveToken: saveToken,
        getUser: getUser,
        getUserFromClient: getUserFromClient
    };
    