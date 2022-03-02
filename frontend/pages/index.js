import {useState} from 'react'

var controller = new AbortController();

export default function Home() {
  const [searchString, setSearchString] = useState("");
  const [autocompletes, setAutocompletes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [suggestionIndex, setSuggestionIndex] = useState(0);
  const [suggestionsActive, setSuggestionsActive] = useState(false);

  function fetchData (search) {
    controller.abort(signal);
    controller = new AbortController();
    let signal = controller.signal;
    if (search === ""){
      setAutocompletes([]);
      setLoading(false);
      setSuggestionsActive(false);
      return;
    }
    setLoading(true);
    fetch("http://localhost:5000/api/search/" + encodeURIComponent(search), { signal })
      .then(res => res.json())
      .then(data => data.filter(item => item != search))
      .then(data => {
        setLoading(false);
        setAutocompletes(data);
        if (data.length > 0){
          setSuggestionsActive(true);
        } else {
          setSuggestionsActive(false);
        }
      })
      .catch(error => {setAutocompletes([]); setLoading(false); setSuggestionsActive(false); console.error(error);})
  }

  function onChange(search) {
    setSearchString(search);
    fetchData(search);
  }

  function handleKeyDown(e) {
    // UP ARROW
    if (e.keyCode === 38) {
      if (suggestionIndex === 0) {
        return;
      }
      setSuggestionIndex(suggestionIndex - 1);
    }
    // DOWN ARROW
    else if (e.keyCode === 40) {
      if (suggestionIndex === autocompletes.length - 1) {
        return;
      }
      setSuggestionIndex(suggestionIndex + 1);
    }
    // ENTER
    else if (e.keyCode === 13) {
      setSearchString(autocompletes[suggestionIndex]);
      setSuggestionIndex(0);
      setSuggestionsActive(false);
    }
    // ESCAPE
    else if (e.keyCode === 27) {
      e.preventDefault();
      setSuggestionsActive(false);
    }
  };

  return (
    <div className="bg-gray-800 h-screen">
      <div className="container mx-auto pt-12 px-24">
        <div className="flex justify-center">
          <div className="text-white text-gray-200 text-xl mr-12 pt-1">URL</div>
          {suggestionsActive && <div className='w-screen h-screen absolute top-0' onClick={() => setSuggestionsActive(false)} />}
          <div className='relative'>
            <input className={"bg-gray-700 text-gray-200 text-xl px-6 py-2 appearance-none focus:outline-none w-[700px] " + (suggestionsActive ? "rounded-t-xl border-b border-gray-600" : "rounded-xl")} type="text" value={searchString} onClick={() =>{if (autocompletes.length > 0) {setSuggestionsActive(true)}}} onChange={(e) => onChange(e.target.value)} onKeyDown={handleKeyDown}></input>
            {loading &&
              <svg xmlns="http://www.w3.org/2000/svg" className='absolute right-6 top-2 animate-spin rotate-180 transform h-6 w-6 text-gray-400' fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            }
            {suggestionsActive &&
              <ul className="absolute bg-gray-700 text-gray-200 rounded-b-xl w-[700px] py-2 overflow-hidden">
                {autocompletes.map((item, index) => {
                  return <li className={"px-6 py-2 hover:bg-gray-600 cursor-pointer text-lg " + (index === suggestionIndex && "bg-gray-600")} key={index} onClick={(e) => onChange(item)}>{item}</li>
                })}
              </ul>
            }
          </div>
        </div>
      </div>
    </div>
  )
}
