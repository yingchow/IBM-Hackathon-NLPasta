import React from 'react'
import styled from 'styled-components'

import { Tag, Tile as CarbonTile } from 'carbon-components-react'


const Tile = styled(CarbonTile)`
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
  margin: 1rem 0;
  padding-left: 22px;
  
  :first-of-type {
    margin: 0 auto auto
  }
`

const SentimentBar = styled.div`
  position: absolute;
  left: 0;
  top: 0;

  height: 100%;
  width: 6px;
  background-color: ${({ sentiment }) => sentiment > 0 ? 'mediumseagreen' : 'tomato' };
`

const Divider = styled.hr`
  width: 100%;
  border: 0;
  border-top: ${({ visible }) => visible ? '1px' : '0px' } solid #ccc;
`

const Content = styled.p`
  padding: 1rem 0;
  font-size: 1.2rem;
  line-height: calc(1.5 + 0);
`

function ReviewCard(props) {
  const { sentiment, user_id, date, topics, text } = props.review

  return (
    <Tile>
      <SentimentBar sentiment={sentiment} />
      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between' }}>
          <div>
            {/* <h1 style={{ display: 'inline', fontSize: '2rem', color: sentiment > 0 ? 'mediumseagreen' : '#dc3545' }}>{sentiment}</h1> */}
            <span>@{user_id}</span>
          </div>
          <span>{date}</span>
        </div>
        <Divider visible/>
        <Content>
          {text}
        </Content>
        <Divider/>
        <div>{topics.map(topic => <Tag key={topic} text={topic} type="gray">{topic}</Tag>)}</div>
      </div>
    </Tile>
  )
}
  
export default ReviewCard