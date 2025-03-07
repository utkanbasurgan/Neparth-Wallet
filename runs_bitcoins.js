//
// Copyright © 2024 by Neparth
//
//--------------------------------------------------------------------------------------------------------------------------------

const args = process.argv.slice(2);
const { Secrets } = require('/home/neparth/neparth_websites/settings_daemons/secrets_settings/apis_secrets.js');
const axios = require('axios');

//--------------------------------------------------------------------------------------------------------------------------------

if (args.length === 0)
  {
    console.error('Error: No address provided.');
    process.exit(1);
}

const address = args[0];
const node = "btcbook.nownodes.io";
const nodeAPIKey = Secrets.NOW_NODES_API;

//--------------------------------------------------------------------------------------------------------------------------------

async function checkBitcoinBalance(address) 
{
    try 
    {
        const response = await axios.get(`https://${node}/api/v2/address/${address}`, 
        {
            headers: 
            {
                'api-key': nodeAPIKey
            }
        });
        
        const balance = response.data.balance;
        console.log(`${(balance / 100000000).toFixed(8)} BTC`);
    } 
    catch (error) 
    {
        console.error('Error fetching balance:', error.response ? error.response.data : error.message);
    }
}

checkBitcoinBalance(address);

//--------------------------------------------------------------------------------------------------------------------------------