# PertDist
A scipy-like implementation of the [PERT distribution](https://en.wikipedia.org/wiki/PERT_distribution).

## Motivation
In my current job I work a fair amount with the PERT (also known as Beta-PERT) distribution, but there's currently no implementation of this in scipy. To make up the deficency I crafted up my own PERT distribution class, leveraging numpy and scipy to properly flesh out the functionality. The API is heavily modeled after the scipy.stats methods API's.

## Build Status
TODO: when I figure out how in blazes to add these ;-)

## Installation
Installation is straightforward: `pip install pertdist`

## Code Example
Usage is very similar to what you would find in a scipy.stats class as well:

```
from pert import PERT
import seaborn as sns

pert = PERT(10, 190, 200)
sns.kdeplot(pert.rvs(10000))
```

On running this you should see a chart of a heavily low/left skewed distribution (recommended running in Jupyter or Spyder).

## Roadmap
* Develop unit tests
    - Especially around flexible identification of various data types, eg: accepting DataFrames, Series, lists, etc.
* Build out the following scipy function analogues:
    - sf
    - logsf
    - ppf
    - isf
    - moment
    - entropy
    - fit
    - expect
    - median
    - mean
    - var
    - std
    - stats (implemented, but needs refinement)
    
A version history is located [here](https://github.com/Calvinxc1/PertDist/blob/master/VersionHistory.md)

## Contributing
Since this is my first published project, I'm pretty relaxed about contributions. Feel free to send me a pull request with any updates/changes/etc you have in mind!

Note that I do follow [Vincent Driessen's Git Branching Model](https://nvie.com/posts/a-successful-git-branching-model/) rather rigorously. If you do contribute, it'll most likely be pulled into the `develop` branch.

Also, I'm rather fond of [Semantic Commit Messages](https://seesparkbox.com/foundry/semantic_commit_messages), but I'm only picky about those for my own contributions, feel free to use wahtever commit message style you'd like.

## License
This project uses the [GNU General Public License](https://github.com/Calvinxc1/PertDist/blob/master/LICENSE).

Short version: Have fun and use it for whatever, just make sure to attribute me for it (-: