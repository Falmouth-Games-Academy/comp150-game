#include "stdafx.h"
#include "PatientGame.h"
#include "InitialisationError.h"
#include "Creature.h"
#include "Guard.h"
#include "Doctor.h"
#include "Player.h"

PatientGame::PatientGame()
	: guardSprite("Sprites\\Guard.png"),
	doctorSprite("Sprites\\Doctor.png"),
	creatureSprite("Sprites\\Creature.png"),
	playerSprite("Sprites\\Player.png"),
	floorSprite("Sprites\\small\\floor.png"),
	verticalWallSprite("Sprites\\small\\ver_wall.png"),
	horizontalWallSprite("Sprites\\small\\horiz_wall.png"),
	verticalDoorSprite("Sprites\\small\\ver_door.png"),
	horizontalDoorSprite("Sprites\\small\\horiz_door.png"),
	exitSprite("Sprites\\small\\exit.png"),
	level(this)

{

	// Initialise SDL video system
	if (SDL_Init(SDL_INIT_VIDEO) < 0)
	{
		throw InitialisationError("SDL_Init failed");
	}

	// Create window for the game
	window = SDL_CreateWindow("The Doomed Patient", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, WINDOW_WIDTH, WINDOW_HEIGHT, SDL_WINDOW_SHOWN); //| SDL_WINDOW_FULLSCREEN
	// Check if window was successfully created
	if (window == nullptr)
	{
		throw InitialisationError("SDL_CreateWindow failed");
	}

	// Create renderer for the game
	renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_PRESENTVSYNC);
	// Check if renderer was successfully created
	if (renderer == nullptr)
	{
		throw InitialisationError("SDL_CreateRenderer failed");
	}


	// For testing
	level.renderer = renderer;
}


PatientGame::~PatientGame()
{
	SDL_DestroyRenderer(renderer);
	SDL_DestroyWindow(window);
	SDL_Quit();
}


void PatientGame::run()
{
	running = true;
	level.generateMaze();
	player = level.createPlayer();

	// Main game loop
	while (running)
	{
		handleEvents();
		update();
		render();
	}
}


// Handle events such as quitting and player input here
void PatientGame::handleEvents()
{
	SDL_Event ev;
	if (SDL_PollEvent(&ev))
	{
		switch (ev.type)
		{
		// Close the game when user quits
		case SDL_QUIT:
			running = false;
			break;

		default:
			break;
		}
	} 

	// Check keyboard state
	const Uint8* keyboardState = SDL_GetKeyboardState(nullptr);
	if (keyboardState[SDL_SCANCODE_UP])
		player->move(Directions::Direction::NORTH);
	if (keyboardState[SDL_SCANCODE_DOWN])
		player->move(Directions::Direction::SOUTH);
	if (keyboardState[SDL_SCANCODE_LEFT])
		player->move(Directions::Direction::WEST);
	if (keyboardState[SDL_SCANCODE_RIGHT])
		player->move(Directions::Direction::EAST);
}


// Game updates that need to happen every frame go here
void PatientGame::update()
{

}


// Render objects and draw them to the screen here
void PatientGame::render()
{
	// Clear the screen
	SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
	SDL_RenderClear(renderer);

	//Render game objects here
	level.render(renderer);

	// Present the newly rendered screen
	SDL_RenderPresent(renderer);
}