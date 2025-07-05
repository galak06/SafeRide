/**
 * Relationship type enum
 */
export enum RelationshipType {
  PARENT = 'parent',
  CHILD = 'child',
  ESCORT = 'escort'
}

/**
 * Parent-child relationship interface
 */
export interface ParentChildRelationship {
  id: string
  parent_id: string
  child_id: string
  escort_id?: string
  relationship_type: RelationshipType
  is_active: boolean
  created_at: string
  updated_at: string
  notes?: string
}

/**
 * Create relationship request interface
 */
export interface ParentChildRelationshipCreate {
  parent_id: string
  child_id: string
  escort_id?: string
  relationship_type: RelationshipType
  notes?: string
}

/**
 * Update relationship request interface
 */
export interface ParentChildRelationshipUpdate {
  escort_id?: string
  is_active?: boolean
  notes?: string
}

/**
 * User relationships interface showing all relationships for a user
 */
export interface UserRelationships {
  user_id: string
  as_parent: ParentChildRelationship[]
  as_child: ParentChildRelationship[]
  as_escort: ParentChildRelationship[]
} 