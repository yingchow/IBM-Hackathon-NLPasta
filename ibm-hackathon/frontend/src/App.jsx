import React, { useEffect, useState } from 'react';
import styled from 'styled-components'
import { getBusinesses, getReviews } from './api';

import Container from './components/Container'
import {
  Header as CarbonHeader,
  HeaderName,
  HeaderNavigation,
  HeaderMenu,
  HeaderMenuItem
} from "carbon-components-react/lib/components/UIShell"
import { Tabs, Tab } from 'carbon-components-react'
import ReviewCard from './components/ReviewCard';


function Header() {
  return (
    <CarbonHeader aria-label="IBM Platform Name">
      <Container>
        <HeaderName href="#" prefix="IBM">
          [Platform]
        </HeaderName>
      {/* <HeaderNavigation aria-label="IBM [Platform]">
        <HeaderMenuItem href="#">Link 1</HeaderMenuItem>
        <HeaderMenuItem href="#">Link 2</HeaderMenuItem>
        <HeaderMenuItem href="#">Link 3</HeaderMenuItem>
        <HeaderMenu aria-label="Link 4" menuLinkName="Link 4">
          <HeaderMenuItem href="#">Sub-link 1</HeaderMenuItem>
          <HeaderMenuItem href="#">Sub-link 2</HeaderMenuItem>
          <HeaderMenuItem href="#">Sub-link 3</HeaderMenuItem>
        </HeaderMenu>
      </HeaderNavigation> */}
      </Container>
    </CarbonHeader>
  )
}

const TabBar = styled(Tabs)`
  ul {
    width: 100%;
  }

  a, a:active, a:focus {
    width: inherit;
  }
`


function TabContent({ reviews }) {
  return (
    <>
      {reviews.map(review => (
        <ReviewCard
          key={review.review_id}
          review={{...review, sentiment: 4, topics: ['food'] }}
        />
      ))}
    </>
  )
}

function App() {
  const [ business, setBusiness ] = useState({ reviews: [] })
  const [ reviews, setReviews ] = useState([])

  useEffect(() => {
    getBusinesses()
      .then(([ first, ..._ ] ) => first)
      .then(business => {
        getReviews(business.business_id).then(setReviews)
        return business
      })
      .then(setBusiness)
  }, [])

  const positive = reviews.filter(review => review.cool > 3)

  const tabs = [
    {
      label: `All Reviews (${reviews.length})`,
      component:<TabContent reviews={reviews} />
    },
    {
      label: `Cool (${positive.length})`,
      component: <TabContent reviews={positive} />
    },
    {
      label: `Negative (${reviews.length})`,
      component:<TabContent reviews={reviews} />
    },
    {
      label: `Questions (${reviews.length})`,
      component:<TabContent reviews={reviews} />
    },
    {
      label: `Concerns (${reviews.length})`,
      component:<TabContent reviews={reviews} />
    },
  ]

  return (
    <div className="App">
      <Header />
      <div id='nav-spacer' style={{ height: 'calc(48px + 1rem)' }} />
      <Container>
        <TabBar>
          {tabs.map(({ label, component }) => <Tab key={label} label={label}>{component}</Tab>)}
        </TabBar>
      </Container>
    </div>
  );
}

export default App;
