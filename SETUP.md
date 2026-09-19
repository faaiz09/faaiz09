# How to put this on your GitHub profile (no coding tools needed)

You can delete this file after setup. Button names may differ slightly on your screen.

1. **Open your profile repository:** github.com/faaiz09/faaiz09
2. **Upload the visible files.** Click **Add file > Upload files**, drag in `README.md`, the `assets` folder and the `scripts` folder, then click **Commit changes**.
3. **Add the three automation files.** For each file inside `.github/workflows/` in this download
   (`arcade.yml`, `profile-3d.yml`, `stats.yml`):
   click **Add file > Create new file**, type the name exactly, for example `.github/workflows/arcade.yml`,
   open the file from this download in Notepad or TextEdit, copy everything, paste it in, and click **Commit changes**.
   If you cannot see the `.github` folder on your computer: on Mac press Cmd + Shift + . in Finder; on Windows turn on View > Hidden items.
   If you uploaded an older `snake.yml` earlier, delete it: `arcade.yml` replaces it.
4. **Allow the automations to save files.** Go to **Settings > Actions > General > Workflow permissions**, choose **Read and write permissions**, and click **Save**.
5. **Run each automation once.** Open the **Actions** tab. Click each of the three workflows on the left, then **Run workflow**. Wait for the green ticks. After this they run by themselves every day.
6. **Check your profile** at github.com/faaiz09 and refresh. The Pac-Man, 3D and stats pictures appear only after step 5 has finished.

## If something shows as a broken image
- Pac-Man, Snake: the "Contribution arcade" workflow has not finished, or failed. Open the run in the Actions tab and read the error.
- 3D calendar: open the `profile-3d-contrib` folder in your repository and check the file names. If the dark one is not called `profile-night-rainbow.svg`, change that name in `README.md`.
- Stats card still says "Run the workflow": run "Profile stats" from the Actions tab.

## Changing the words inside the animated pictures
Edit the lists at the top of `scripts/build_assets.py` (roles, stations, terminal lines, system map, toolbox), then run `python3 scripts/build_assets.py` and upload the new `assets` folder. Or ask Claude to regenerate them for you.
