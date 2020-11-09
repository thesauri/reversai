import React, { useState } from 'react'
import Group from './Group'

const TournamentInfo = ({ matchHistory, groups }) => {
  const [botPoints, setBotPoints] = useState({})

  const getPoints = (matchHistory) => {
    const bots = {}

    const assignPoints = (black, white) => {
      let blackPoints
      let whitePoints
      if (black.score === white.score) {
        blackPoints = 1
        whitePoints = 1
      } else if (black.score > white.score) {
        blackPoints = 3
        whitePoints = 0
      } else {
        blackPoints = 0
        whitePoints = 3
      }
      if (bots[black.name] === undefined) {
        bots[black.name] = 0
      }
      if (bots[white.name] === undefined) {
        bots[white.name] = 0
      }
      bots[black.name] += blackPoints
      bots[white.name] += whitePoints
    }

    matchHistory.forEach(game => {
      assignPoints(game.black, game.white)
    })

    return bots
  }

  // Fill bot score info into a list of groups, based on a bot dict with
  // the format { botName1: score, botName2: score }
  const fillInfo = (bots, groups) => {
    return groups.map(group => {
      return group
        .map(name => {
          return {
            name,
            points: bots[name] ? bots[name] : 0
          }
        })
        .sort((bot1, bot2) => {
          return bot1.points < bot2.points
        })
    })
  }

  const getStandings = (matchHistory, groups) => {
    // Calculate annotations based on previous positions.
    const prevPoints = getPoints(matchHistory.slice(0, matchHistory.length - 1))
    const prevStandings = fillInfo(prevPoints, groups)
    const newPoints = getPoints(matchHistory)
    const newStandings = fillInfo(newPoints, groups)
  
  const annotatedStandings = newStandings
    .map((newGroupStandings, groupIndex) => {
      const prevGroupStandings = prevStandings[groupIndex].map(b => b.name)
      return {
        standings: newGroupStandings.map((bot, botIndex) => {
          if (prevGroupStandings.includes(bot.name)) {
            const oldIndex = prevGroupStandings.indexOf(bot.name)
            if (botIndex !== oldIndex) {
              bot.annotation = botIndex < oldIndex ? 'up' : 'down'
            }
          }
          return bot
        }),
        groupId: groups[groupIndex].reduce((a, b) => a + b)
      }
    })
    return annotatedStandings
  }

  const annotatedStandings = getStandings(matchHistory, groups)

  return (
    <div>
      {annotatedStandings.map((group, index) => {
        return <Group standings={group.standings} key={group.groupId} number={index+1} />
      })}
    </div>
  )
}

export default TournamentInfo
