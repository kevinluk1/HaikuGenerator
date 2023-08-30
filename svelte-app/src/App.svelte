<script>
  import { onMount } from 'svelte';
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


  async function handleGenerateButtonClick() {
  	startSpeaking()
  	try{
  		console.log("Fetching Haiku")

  		const response = await fetch('http://localhost:5000/generate',
				{credentials:'include'})
		const data = await response.json()


		firstLine = data['line1']
		showFirstLine = true;
  		setTimeout(()=> {
  			secondLine = data['line2'];
			showSecondLine = true;
			setTimeout(() => {
				thirdLine = data['line3'];
				showThirdLine = true;}, 1000);
		}, 1000)
		animationRemount()
	} catch(error){
  		console.error("Error fetch data:", error);
	}
  }


  function animationRemount(){
  	showFirstLine = false; // force remount to allow for animation to occur on new poem generation
        setTimeout(() => {
          showFirstLine = true;
        }, 0);

	  	showSecondLine = false; // force remount to allow for animation to occur on new poem generation
        setTimeout(() => {
          showSecondLine = true;
        }, 1000);

	  showThirdLine = false; // force remount to allow for animation to occur on new poem generation
        setTimeout(() => {
          showThirdLine = true;
        }, 2000);
  }

  async function handleRegen2ButtonClick(){
  	try{
  		console.log("Regen line 2")
		const response = await fetch('http://localhost:5000/regen2', {credentials:'include'})
		const data = await response.json()
		finalHaiku = (`\n\n ${data['line1']} \n ${data['line2']} \n ${data['line3']}`);
  		console.log(finalHaiku)
  		showHaiku = false
        setTimeout(() => {
          showHaiku = true;
        }, 0);

	}
	catch(error){
  		console.error(error)
	}
  }

  async function handleRegen3ButtonClick(){
  	try{
  		console.log("Regen line 3")
		const response = await fetch('http://localhost:5000/regen3', {credentials:'include'})
		const data = await response.json()
		finalHaiku = (`\n\n ${data['line1']} \n ${data['line2']} \n ${data['line3']}`);
  		console.log(finalHaiku)
  		showHaiku = false
        setTimeout(() => {
          showHaiku = true;
        }, 0);

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
			<img src="/poet.jpg" alt="Poet" class:shake-animation={speaking}>
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

</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}
	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 3em;
		font-weight: 100;
		font-family: 'Courier New', Courier, monospace; /* A typewriter-like font */
	}

	@keyframes typewriter {
  		0% { width: 0; }
  		100% { width: 100%; }
	}
	pre {

	}
	@keyframes shake {
    0% { transform: translate(1px, 1px) rotate(0deg); }
    10% { transform: translate(-1px, -2px) rotate(-1deg); }
    20% { transform: translate(-2px, 0px) rotate(1deg); }
    30% { transform: translate(1px, 2px) rotate(0deg); }
    40% { transform: translate(1px, -1px) rotate(1deg); }
    50% { transform: translate(-1px, 2px) rotate(-1deg); }
    60% { transform: translate(-1px, 1px) rotate(0deg); }
    70% { transform: translate(2px, 1px) rotate(-1deg); }
    80% { transform: translate(-1px, -1px) rotate(1deg); }
    90% { transform: translate(2px, 2px) rotate(0deg); }
    100% { transform: translate(1px, -2px) rotate(-1deg); }
}

	.haikuLine{
		text-align: center;
		font-size: 2.0em;
	  	white-space: nowrap;
	  	font-family: 'Courier', Courier, monospace;
	    display: inline-block;
	    overflow: hidden;
	    max-width: 100%;
	}

	.haikuLine:nth-child(1) {
  animation: typewriter 1s steps(30, end) 1s 1 normal both;
}

.haikuLine:nth-child(2) {
  animation: typewriter 1s steps(30, end) 1s 1 normal both;
}

.haikuLine:nth-child(3) {
  animation: typewriter 1s steps(30, end) 1s 1 normal both;
}
.shake-animation {
    animation: shake 0.5s;
    animation-iteration-count: infinite;
}
	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
