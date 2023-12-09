let container = document.querySelector('#container');

function App(props) {
    const renderButton = () => {
        if (props.inPlaylist) {
          return "Remove from playlist";
        } else {
          return "Add to playlist";
        }
      }

    const updateDatabase = () => {
        fetch('/playlist', {
            method: 'PUT',
            body: JSON.stringify({
                artist: props.artist,
                title: props.title,
                albumUrl: props.image,
                uri: props.uri
            })
        })
        if (props.inPlaylist == true){
            props.inPlaylist = false
            document.getElementById(props.uri).innerHTML = 'Add to playlist'
        }
        else{
            props.inPlaylist = true
            document.getElementById(props.uri).innerHTML = 'Remove from playlist'
        }
    }
  
    return (
        <div 
            className = "d-flex m-3 align-items-center"
            style = {{cursor: 'pointer'}}
            onClick = {() => changePlayer(props.uri)}
        >
            <img src = {props.image} style = {{height: '100px', width: '100px'}}/>
            <div className = "ml-4">
                <div>{props.title}</div>
                <div className = "text-muted">{props.artist}</div>
                {/* <form action = {() => updateDatabase()} method = 'POST'>
                    <input type = 'hidden' name = 'artist' value = {props.artist}/>
                    <input type = 'hidden' name = 'title' value = {props.title}/>
                    <input type = 'hidden' name = 'albumUrl' value = {props.image}/>
                    <input type = 'hidden' name = 'uri' value = {props.uri}/>
                    {renderButton()}
                </form> */}
                <button id = {props.uri} style={{color: 'white', backgroundColor: '#3081D0'}} onClick = {() => updateDatabase()}>{renderButton()}</button>
            </div>
        </div>
    );
}

function changePlayer(uri){
    console.log(uri)
    ReactDOM.render(
        <iframe src= {"https://open.spotify.com/embed/track/" + uri} width="100%" height="200" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>, 
    document.getElementById('musicPlayer'))
}

for (let i = 0; i < window.songData.length; i++) {
    const id = i
    const d = document.createElement("div")
    d.id = id
    container.append(d) 
    
    ReactDOM.render(<App title = {window.songData[i]['title']} artist = {window.songData[i]['artist']} image={window.songData[i]['albumUrl']} uri = {window.songData[i]['uri']} inPlaylist = {window.songData[i]['inPlaylist']} />, document.getElementById(id))
}