import { Bar } from './bar.js';

(function(){
    //console.log( 'hello world!' )
    d3.json( '/load_data' )
        .then( data => main( data ) )
        .catch( err => console.error( err ) );
})();

// Global Variables
function main( data ) {
    // Input to main
    d3.select( "#users" )
        .append( "span" )
        .text( data.users.length )

    let	bars = new Bar( data, 'vis1' );
}
