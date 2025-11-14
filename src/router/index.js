import { createRouter, createWebHistory } from 'vue-router'
import TeamPresentation from '../components/TeamPresentation.vue'
import GraphGenerator from '../components/GraphGenerator.vue'
import GraphVisualization from '../components/GraphVisualization.vue'

const routes = [
    {
        path: '/',
        name: 'Team',
        component: TeamPresentation
    },
    {
        path: '/generator',
        name: 'Generator',
        component: GraphGenerator
    },
    {
        path: '/visualization',
        name: 'Visualization',
        component: GraphVisualization
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router