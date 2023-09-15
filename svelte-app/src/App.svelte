<script>
  let title = "Markov-Chain Haiku Generator";
  let finalHaiku = ""

  let showHaiku = false;
  let speaking = false;
  let firstLine = ""
  let secondLine = ""
  let thirdLine = ""
  let showFirstLine = false;
  let showSecondLine = false;
  let showThirdLine = false;

	function displayHaiku(data){
		firstLine = data['line1']
		showFirstLine = true;
		setTimeout(()=> {
			secondLine = data['line2'];
			showSecondLine = true;
			setTimeout(() => {
				thirdLine = data['line3'];
				showThirdLine = true;}, 1000);
		}, 1000)
  	}
	function newHaikuAnimationRemount(){
	showFirstLine = false; // force remount to allow for animation to occur on new poem generation
		setTimeout(() => {
		  showFirstLine = true;
		}, 0);
		showSecondLine = false;
		setTimeout(() => {
		  showSecondLine = true;
		}, 1000);
	  showThirdLine = false;
		setTimeout(() => {
		  showThirdLine = true;
		}, 2000);
	}
	async function handleGenerateButtonClick() {
	startSpeaking()
	try{
		console.log("Fetching Haiku")
		const response = await fetch('https://backend-hf70.onrender.com/generate',
				{credentials:'include'})
		const data = await response.json()
		displayHaiku(data)
		newHaikuAnimationRemount()
	} catch(error){
		console.error("Error fetch data:", error);
		}
	}
	async function handleRegen2ButtonClick(){
	try{
		startSpeaking()
		console.log("Regen line 2")
		const response = await fetch('https://backend-hf70.onrender.com/regen2', {credentials:'include'})
		const data = await response.json()
		secondLine = data['line2']
		showSecondLine = false;
		setTimeout(() => {
		  showSecondLine = true;
		}, 1000);

		}
	catch(error){
		console.error(error)
		}
	}
  async function handleRegen3ButtonClick(){
  	try{
  		startSpeaking()
  		console.log("Regen line 3")
		const response = await fetch('https://backend-hf70.onrender.com/regen3', {credentials:'include'})
		const data = await response.json()
		thirdLine = data['line3']
		showThirdLine = false;
  		setTimeout(() => {
		  showThirdLine = true;
		}, 1000);
		}
	catch(error){
  		console.error(error)
		}
	}

  function startSpeaking() {
        speaking = true;
        setTimeout(() => {
            speaking = false;
        }, 2000);
    }
</script>
<main>
	<h1>{title}</h1>
		<div>
			<img src="/guy.gif" alt="rapGod" class:shake-animation={speaking}>
		</div>
	<div class="haikuLines">
		{#if showFirstLine}
			<div class="haikuLine">{firstLine}</div>
		{/if}
		{#if showSecondLine}
			<div class="haikuLine">{secondLine}</div>
		{/if}
		{#if showThirdLine}
			<div class="haikuLine">{thirdLine}</div>
		{/if}
	</div>
	<div>
		<div class="buttonBox">
			<div>
				<button on:click={handleGenerateButtonClick}>Generate</button>
			</div>
			<div>
				<button on:click={handleRegen2ButtonClick}>Regenerate Line 2</button>
			</div>
			<div>
				<button on:click={handleRegen3ButtonClick}>Regenerate Line 3</button>
			</div>
		</div>
	</div>
	<div class="explanation">
		<blockquote>
			<strong>
				NOTE: Markov chains sometimes strongly favor certain transitions, which can lead to the same line being regenerated.
			</strong>
		</blockquote>
		<p>
			Although the training corpus for this generator is based on roughly 300 different ancient and modern Haikus, this generator highlights the somewhat  annoying nature of the Markov chain model when provided with limited training data.
		</p>
		<h2>
			What is a Markov Chain? 🤔
		</h2>
		<p>
			A Markov chain is a mathematical model used to describe systems where the probability of each event occurring only depends on the state attained in the previous event. It's a way to make predictions based on past data, but only the most recent data is considered for making future predictions.
		</p>
		<p>
			In this case, a Markov chain is employed to predict the next word in a line of the poem based on one or more preceding words. The "states" in this case would be the words themselves, and the "transitions" between states would be governed by how often different words tend to follow one another in a training corpus of existing Haikus.
		</p>
	</div>
</main>