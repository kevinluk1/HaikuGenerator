

<script>
  import { onMount } from 'svelte';
  let message = "Haiku Generator";

  onMount(async () => {
      try {
          const response = await fetch("http://localhost:5000/hello");
          const data = await response.json();
          name = data.message;
      } catch (err) {
          name = "Failed to fetch data";
      }
  });

  async function handleGenerateButtonClick() {
  	try{
  		console.log("Fetching Haiku")
  		const response = await fetch('http://localhost:5000/generate')
		const data = await response.json()
		console.log(data)
	} catch(error){
  		console.error("Error fetch data:", error);
	}
  }
</script>




<main>
	<h1>{message}</h1>
	<button on:click={handleGenerateButtonClick}>Generate</button>
	<h1>Hello {name}!</h1>

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
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>