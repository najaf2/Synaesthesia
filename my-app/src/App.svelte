<script>
	let searchInput;
	async function search() {
		console.log(searchInput.value);
		console.log(selectedGenres)

		const selectedGenreIds = selectedGenres.map((genre) => genre.id);
		const selectedGenreQuery = selectedGenreIds.join(" ");
		const response = await fetch(
			`http://localhost:5000/search?q=${searchInput.value}&genres=${selectedGenreQuery}`
		);
		const data = await response.text();
		results.innerHTML = data;
	}

	function submit(event) {
		event.preventDefault();
		search();
	}

	let genres = [
		{ id: "pop", label: "Pop" },
		{ id: "hiphop", label: "Hip Hop" },
		{ id: "rock", label: "Rock" },
		{ id: "edm", label: "EDM" },
		{ id: "country", label: "Country" },
	];
	let selectedGenres = [];
	function updateSelectedGenres(event) {
		const genreId = event.target.value;
		const isChecked = event.target.checked;

		if (isChecked) {
			selectedGenres = [...selectedGenres, genreId];
		} else {
			selectedGenres = selectedGenres.filter((id) => id !== genreId);
		}
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
	<div class="genre-checkboxes">
		{#each genres as genre}
			<label class="genre-checkbox">
				<input
					type="checkbox"
					value={genre.id}
					on:change={updateSelectedGenres}
					checked={selectedGenres.includes(genre.id)}
				/>
				<span class="checkmark" />
				{genre.label}
			</label>
		{/each}
	</div>
</div>

<div class="results-container">
	<div class="results" id="results" />
</div>

<style>
	:global(body) {
		background-color: #191414;
	}
	.results-container {
		margin-top: 20vh;
		margin-bottom: 50px;
		display: flex;
		justify-content: center;
	}

	.results {
		margin-top: 10px;
		margin-bottom: 50px;
		min-width: 75%;
		display: flex;
		align-items: center;
		flex-direction: column;
		gap: 30px;
	}
	.search-form {
		display: flex;
		flex-direction: column;
		align-items: center;
		/* margin-bottom: 20vh; */
		margin-top: 20vh;
	}

	.search-input {
		padding: 10px;
		border: 1px solid #ddd;
		border-radius: 5px;
		margin-right: 10px;
		font-size: 16px;
		width: 250px;
	}

	.search-button {
		padding: 10px;
		border: 1px solid #ddd;
		border-radius: 5px;
		background-color: #1db954;
		color: white;
		font-size: 16px;
		cursor: pointer;
	}

	.genre-checkboxes {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		margin-top: 10px;
	}

	.genre-checkbox {
		display: flex;
		align-items: center;
		margin-right: 10px;
		margin-bottom: 10px;
		font-size: 16px;
		color: #b3b3b3;
		cursor: pointer;
	}

	.genre-checkbox input[type="checkbox"] {
		display: none;
	}

	.genre-checkbox .checkmark {
		display: inline-block;
		width: 20px;
		height: 20px;
		border: 1px solid #b3b3b3;
		border-radius: 50%;
		margin-right: 10px;
		position: relative;
	}

	.genre-checkbox .checkmark::after {
		content: "";
		display: none;
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 10px;
		height: 10px;
		border-radius: 50%;
		background-color: #1db954;
	}
	.genre-checkbox input[type="checkbox"]:checked + .checkmark::after {
		display: block;
	}
</style>
