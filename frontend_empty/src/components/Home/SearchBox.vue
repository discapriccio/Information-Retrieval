<template>
	<div class="search-box">
		<div class="search">
			<input
				@focus="focusShow"
				@blur="blurShow"
				@keyup.enter="enterToSearch"
				class="input-box"
				type="text"
				placeholder="Search..."
				v-model="searchQuery"
			/>
			
		</div>
		<!-- {{searchedsuggests}} -->
        <div
			class="suggests"
			v-show="show && searchedsuggests.list.length != 0"
			@mouseenter="isMouseOnSerchBox = true"
			@mouseleave="isMouseOnSerchBox = false"
		>
			<div
				class="suggest-item"
			>

			</div>
		</div>
		
	</div>
</template>

<script>

</script>

<style lang="less" scoped>
.search-box {
	background-color: #fff;
	width: 5rem;
	margin: auto;
	border-radius: 0.2rem;
	box-shadow: 0.05rem 0.05rem 0.1rem #666;
	.search {
		display: block;
		position: relative;
		left: 0;
		top: 0;
		width: 5rem;
		margin: auto;
		.input-box {
			width: 5rem;
			height: 0.4rem;
			padding: 0 0.5rem 0 0.2rem;
			color: #111;
			font-size: 0.2rem;
			border-radius: 0.2rem;
			border: 0;
			// box-shadow: 0.05rem 0.05rem 0.05rem #666;
			outline: none;
		}
		.icon {
			position: absolute;
			top: 0.05rem;
			right: 0.1rem;
			height: 0.3rem;
			width: 0.3rem;
			fill: #9370DB;
		}
	}
	.suggests {
		padding-bottom: 0.15rem;
		margin: 0 0.1rem 0 0.1rem;
		border-top: #ccc 1px solid;
		.suggest-item {
			margin-top: 0.1rem;
			height: 0.3rem;
			padding-left: 0.1rem;
			cursor: pointer;
			display: flex;
			justify-content: left;
			align-items: center;
			.icon {
				height: 0.15rem;
				width: 0.15rem;
				fill: #9370DB;
			}
			.text {
				width: 4.3rem;
				padding-left: 0.1rem;
				line-height: 0.3rem;
				overflow: hidden;
				text-overflow: ellipsis;
				display: -webkit-box;
				-webkit-box-orient: vertical;
				-webkit-line-clamp: 1;
				text-align: left;
			}
		}
	}
}
</style>
