<script>
  import { onMount } from 'svelte';
  let title = "Markov-Chain Haiku Generator";
  let finalHaiku = ""
  let showHaiku = false;
  let speaking = false;

  onMount(async () => {
  try {
	  const response = await fetch("http://localhost:5000/hello");
	  const data = await response.json();
	  name = data.message;
  }
  catch (err) {
	  name = "Failed to fetch data";
  }
  });
  async function handleGenerateButtonClick() {
  	startSpeaking()
  	try{
  		console.log("Fetching Haiku")
  		const response = await fetch('http://localhost:5000/generate')
		const data = await response.json()
		finalHaiku = (`\n\n ${data['line1']} \n ${data['line2']} \n ${data['line3']}`);
		console.log(finalHaiku)

		showHaiku = false; // force remount to allow for animation to occur on new poem generation
        setTimeout(() => {
          showHaiku = true;
        }, 0);

	} catch(error){
  		console.error("Error fetch data:", error);
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
	{#if showHaiku}
		<pre>{finalHaiku}</pre>
	{/if}
	<div>
		<button on:click={handleGenerateButtonClick}>Generate</button>
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
	  font-size: 2.0em;
	  font-family: 'Courier New', Courier, monospace;
	  white-space: pre-wrap;
	  display: inline-block; /* Required for animation to work properly */
	  overflow: hidden; /* Hides the content that overflows the box */
	  animation: typewriter 5s steps(30, end); /* Apply the animation */
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
