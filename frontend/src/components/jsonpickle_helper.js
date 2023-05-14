// To decode the serialized graph, we need to know what each py/id refers to.
// jsonpickle avoids circular references by putting each object in a list the first time it is encountered.
// Subsequent references to the same object are replaced with a py/id that refers to the object's index in the list.
// Thus, if we create our own list of objects in the same order as the jsonpickle list, we can index into it to find the object.

function jsonpickleWouldHaveGivenPyId(obj) {
  // Python dicts, objects, arrays, and tuples all get py/ids - only the first time they are serialized.
  // Python primitives (strings, numbers, etc) do not.

  if (obj === null) {
    return false;
  }
  // Primitives don't get a py/id.
  if (!(obj instanceof Object)) {
    return false;
  }
  // Arrays don't get a py/id.
  if (obj instanceof Array) {
    return true;
  }
  // If obj has a py/id, it must have been serialized before.
  if (obj.hasOwnProperty("py/id")) {
    return false;
  }
  // If obj is empty, it won't get a py/id.
  if (Object.keys(obj).length === 0) {
    return false;
  }
  // If obj is a tuple, it won't get a py/id (the array inside will get one though!).
  if (obj.hasOwnProperty("py/tuple")) {
    return false;
  }

  // Otherwise, obj must be a dict or an object, and it will get a py/id.
  return true;
}

// Depth-first traverse the serialized graph to find all objects in the order they would have appeared in the jsonpickle list.
function getObjectsInOrder(obj) {
  let objects = [];
  if (obj === null) {
    return objects;
  }

  // First add obj, if it should have gotten a py/id.
  if (jsonpickleWouldHaveGivenPyId(obj)) {
    objects.push(obj);
  }

  // Then recursively add all of obj's children.
  if (obj instanceof Array) {
    for (let i = 0; i < obj.length; i++) {
      objects = objects.concat(getObjectsInOrder(obj[i]));
    }
  } else if (obj instanceof Object) {
    for (let key in obj) {
      objects = objects.concat(getObjectsInOrder(obj[key]));
    }
  }
  return objects;
}

export default getObjectsInOrder;
