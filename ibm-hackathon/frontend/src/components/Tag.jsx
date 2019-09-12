import React from 'react'
import styled from 'styled-components'

import { Tag } from 'carbon-components-react'


const Chip = styled.span`
  display: inline-block;
  background-color: #f3f3f3;
  padding: 5px 0.5rem;
  margin: 0 0 0 1rem;
  min-height: 1rem;

  :first-of-type {
    margin: 0;
  }
`

function Tag(props) {
  const { text, type } = props

  return <Tag>{text}</Tag>
}

export default Tag