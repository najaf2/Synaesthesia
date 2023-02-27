<script>
	let searchInput;
	async function search() {
		console.log(searchInput.value);
		const response = await fetch(
			`http://localhost:5000/search?q=${searchInput.value}`
		);
		const data = await response.text();
		results.innerHTML = data;
	}

	function submit(event) {
		event.preventDefault();
		search();
	}
</script>

<div class="search-form">
	<form on:submit={submit}>
		<input
			type="text"
			placeholder="Search for a mood/vibe"
			class="search-input"
			bind:this={searchInput}
		/>
		<button type="submit" class="search-button">Search</button>
	</form>
</div>

<div class="results-container">
	<div class="results" id="results" />
</div>

<style>
	:global(body) {
		background-color: #191414;
	}

	.search-form {
		display: flex;
		justify-content: center;
		margin-top: 100px;
	}

	.search-input {
		font-size: 1.5rem;
		padding: 10px;
		width: 400px;
		border-radius: 20px 0 0 20px;
		border: none;
		outline: none;
	}

	.search-button {
		font-size: 1.5rem;
		padding: 10px 20px;
		background-color: #1db954;
		color: #ffffff;
		border: none;
		border-radius: 0 20px 20px 0;
		cursor: pointer;
		outline: none;
	}

	.results-container {
		margin-top: 50px;
		margin-bottom: 50px;
		display: flex;
		justify-content: center;
	}

	.results {
		margin-top: 50px;
		margin-bottom: 50px;
		min-width: 75%;
		display: flex;
		align-items: center;
		flex-direction: column;
		gap: 30px;
	}
</style>
